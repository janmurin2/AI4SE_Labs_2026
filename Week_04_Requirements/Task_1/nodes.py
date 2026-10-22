"""Nodes of the requirements-refinement network.

Deterministic nodes: load_corpus, coverage_check, render.
LLM nodes:           extract, cluster, write, review.
"""

import json
import operator
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

import config
import prompts
from schemas import (Candidate, ClusteringResult, ClusterPatch, ExtractionResult, Requirement,
                     ReviewResult, SourceDocument, Specification, WrittenRequirement)


class GraphState(TypedDict, total=False):
    input_dir: str
    max_iterations: int
    documents: list[SourceDocument]
    candidates: list[Candidate]
    clusters: ClusteringResult
    coverage: dict
    written: dict[tuple[str, ...], WrittenRequirement]  # cache keyed by the cluster's candidate IDs
    spec: Specification
    review: ReviewResult
    best: dict  # {"spec", "coverage", "entry"} of the best-scoring iteration
    iteration: int
    review_log: Annotated[list[dict], operator.add]
    document: str


def _llm(model: str, schema):
    return ChatOpenAI(model=model, timeout=config.LLM_TIMEOUT_S, max_retries=3).with_structured_output(schema)


def _log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


# --- load_corpus (deterministic) ------------------------------------------

_MONTH_DATE = re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|"
                         r"November|December)\s+\d{1,2},\s+\d{4}")


def _detect_date(path: Path, text: str) -> str | None:
    if m := re.search(r"\d{4}-\d{2}-\d{2}", path.name):
        return m.group(0)
    if m := re.search(r"^Date:\s*(.+)$", text, re.MULTILINE):
        try:
            return parsedate_to_datetime(m.group(1).strip()).date().isoformat()
        except (TypeError, ValueError):
            pass
    if m := _MONTH_DATE.search(text[:3000]):
        return datetime.strptime(m.group(0).replace("  ", " "), "%B %d, %Y").date().isoformat()
    return None


def _detect_kind(path: Path) -> str:
    name = path.name.lower()
    if path.suffix.lower() == ".eml":
        return "email thread"
    for needle, kind in [("minutes", "meeting minutes"), ("meeting", "meeting minutes"),
                         ("interview", "interview"), ("survey", "survey results"),
                         ("srs", "draft requirements specification"), ("spec", "draft requirements specification"),
                         ("reference", "reference documentation")]:
        if needle in name:
            return kind
    return "document"


def load_corpus(state: GraphState) -> dict:
    root = Path(state["input_dir"])
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in config.SUPPORTED_EXTENSIONS)
    if not files:
        raise FileNotFoundError(f"No {sorted(config.SUPPORTED_EXTENSIONS)} files found in {root}")
    docs = []
    for p in files:
        text = p.read_text(encoding="utf-8", errors="replace")
        docs.append(SourceDocument(doc_id=p.relative_to(root).as_posix(), kind=_detect_kind(p),
                                   date=_detect_date(p, text), text=text))
    _log(f"load_corpus: {len(docs)} documents")
    return {"documents": docs, "iteration": 0}


# --- extract (LLM, per document chunk) ---------------------------------------

def _chunks(text: str, size: int) -> list[str]:
    if len(text) <= size:
        return [text]
    parts, current = [], ""
    for para in re.split(r"\n\s*\n", text):
        if current and len(current) + len(para) > size:
            parts.append(current)
            current = ""
        current += para + "\n\n"
    return parts + [current] if current.strip() else parts


def extract(state: GraphState) -> dict:
    if state.get("candidates"):  # supplied via --reuse-candidates
        _log(f"extract: reusing {len(state['candidates'])} previously extracted candidates")
        return {}
    jobs = []  # (doc, messages)
    for doc in state["documents"]:
        pieces = _chunks(doc.text, config.CHUNK_CHARS)
        for i, piece in enumerate(pieces, 1):
            header = (f"Document: {doc.doc_id}\nKind: {doc.kind}\nDate: {doc.date or 'unknown'}"
                      + (f"\nPart {i} of {len(pieces)}" if len(pieces) > 1 else ""))
            jobs.append((doc, [SystemMessage(prompts.clean(prompts.EXTRACT_SYSTEM)),
                               HumanMessage(f"{header}\n\n---\n{piece}")]))
    _log(f"extract: {len(jobs)} chunks with {config.EXTRACT_MODEL}")
    results = _llm(config.EXTRACT_MODEL, ExtractionResult).batch(
        [msgs for _, msgs in jobs], config={"max_concurrency": config.EXTRACT_CONCURRENCY})

    # Deterministic tagging: unique candidate IDs + source document (basis for OS2/OS4/OS8).
    candidates = []
    for (doc, _), result in zip(jobs, results):
        for req in result.requirements:
            candidates.append(Candidate(cid=f"C-{len(candidates) + 1:03d}", doc_id=doc.doc_id,
                                        doc_date=doc.date, **req.model_dump()))
    _log(f"extract: {len(candidates)} candidate requirements")
    return {"candidates": candidates}


# --- cluster (LLM) -----------------------------------------------------------

def _candidate_lines(candidates: list[Candidate], with_source: bool = True) -> str:
    rows = []
    for c in candidates:
        row = {"id": c.cid, "title": c.title, "statement": c.statement, "type": c.type,
               "status": c.source_status}
        if with_source:
            row |= {"doc": c.doc_id, "date": c.doc_date}
        rows.append(json.dumps(row, ensure_ascii=False))
    return "\n".join(rows)


def _norm_cid(cid: str) -> str:
    """Models sometimes write 'C034' instead of 'C-034'."""
    m = re.fullmatch(r"C-?(\d+)", cid.strip())
    return f"C-{int(m.group(1)):03d}" if m else cid.strip()


def _apply_patch(previous: ClusteringResult, patch: ClusterPatch) -> ClusteringResult:
    upserts = {r.key: r for r in patch.upserts}
    claimed = {_norm_cid(cid) for r in patch.upserts for cid in r.candidate_ids}
    reqs = []
    for r in previous.requirements:
        if r.key in patch.removed_keys:
            continue
        if r.key in upserts:
            reqs.append(upserts.pop(r.key))
        else:  # untouched: keep, minus candidates the patch moved elsewhere
            reqs.append(r.model_copy(update={"candidate_ids": [c for c in r.candidate_ids if _norm_cid(c) not in claimed]}))
    reqs += upserts.values()  # newly added requirements
    return ClusteringResult(glossary=patch.glossary, requirements=reqs, discarded=patch.discarded)


def cluster(state: GraphState) -> dict:
    iteration = state.get("iteration", 0) + 1
    parts = [f"CANDIDATE REQUIREMENTS ({len(state['candidates'])}, one JSON object per line):\n"
             + _candidate_lines(state["candidates"])]
    system = prompts.clean(prompts.CLUSTER_SYSTEM)
    _log(f"cluster: iteration {iteration} with {config.CLUSTER_MODEL}")
    if iteration == 1:
        result = _llm(config.CLUSTER_MODEL, ClusteringResult).invoke([SystemMessage(system), HumanMessage(parts[0])])
    else:
        # Revisions are patches applied in code, so a bad revision cannot silently drop untouched requirements.
        parts.append("PREVIOUS VERSION:\n" + state["clusters"].model_dump_json())
        parts.append("AUTOMATIC COVERAGE CHECK:\n" + json.dumps(state["coverage"]))
        parts.append("REVIEWER FEEDBACK:\n" + state["review"].model_dump_json(indent=1))
        patch = _llm(config.CLUSTER_MODEL, ClusterPatch).invoke(
            [SystemMessage(system + "\n" + prompts.CLUSTER_REVISE_INSTRUCTIONS), HumanMessage("\n\n".join(parts))])
        _log(f"cluster: patch with {len(patch.upserts)} upserts, {len(patch.removed_keys)} removals")
        result = _apply_patch(state["clusters"], patch)
    _log(f"cluster: {len(result.requirements)} requirements, {len(result.discarded)} discarded")
    return {"clusters": result, "iteration": iteration}


# --- coverage_check (deterministic) -------------------------------------------

def coverage_check(state: GraphState) -> dict:
    """Repairs what can be repaired safely and reports the rest to the reviewer and the next cluster round."""
    all_ids = {c.cid for c in state["candidates"]}
    cons = state["clusters"]
    seen, keys, repaired = set(), set(), Counter()
    next_key = max((int(m.group(1)) for r in cons.requirements if (m := re.fullmatch(r"K(\d+)", r.key))), default=0) + 1

    def dedupe(ids: list[str]) -> list[str]:
        out = []
        for cid in map(_norm_cid, ids):
            if cid not in all_ids:
                repaired["unknown_candidate_ids_removed"] += 1
            elif cid in seen:  # first occurrence wins; requirements come before discards
                repaired["duplicate_candidate_uses_removed"] += 1
            else:
                seen.add(cid)
                out.append(cid)
        return out

    reqs = []
    for r in cons.requirements:
        ids = dedupe(r.candidate_ids)
        if not ids:
            repaired["empty_requirements_removed"] += 1
            continue
        key = r.key
        if key in keys:
            key, next_key = f"K{next_key:03d}", next_key + 1
            repaired["duplicate_keys_renamed"] += 1
        keys.add(key)
        reqs.append(r.model_copy(update={"key": key, "candidate_ids": ids}))
    discarded = [d.model_copy(update={"candidate_ids": ids}) for d in cons.discarded if (ids := dedupe(d.candidate_ids))]

    names = Counter(r.name.strip().lower() for r in reqs)
    coverage = {
        "missing_candidates": sorted(all_ids - seen),
        "duplicate_names": sorted(n for n, k in names.items() if k > 1),
    }
    coverage["ok"] = not any(coverage.values())
    coverage["auto_repaired"] = dict(repaired)
    _log("coverage_check: " + ("OK" if coverage["ok"] else
                               ", ".join(f"{k}={len(v)}" for k, v in coverage.items() if k != "ok" and v
                                         and k != "auto_repaired"))
         + (f" (auto-repaired: {dict(repaired)})" if repaired else ""))
    return {"clusters": ClusteringResult(glossary=cons.glossary, requirements=reqs, discarded=discarded),
            "coverage": coverage}


# --- write (LLM, one call per requirement) --------------------------------------

def write(state: GraphState) -> dict:
    cons, cands = state["clusters"], {c.cid: c for c in state["candidates"]}
    cache = dict(state.get("written") or {})
    issues_by_key = defaultdict(list)
    if state.get("review"):
        for issue in state["review"].issues:
            for key in issue.keys:
                issues_by_key[key].append(f"{issue.kind}: {issue.description} Suggested fix: {issue.suggested_fix}")
    glossary = "\n".join(f"- {g.term}: {g.definition} (avoid: {', '.join(g.avoid) or '-'})" for g in cons.glossary)

    # Only (re)write requirements that are new, changed membership, or were criticised by the reviewer.
    todo = [r for r in cons.requirements
            if tuple(r.candidate_ids) not in cache or issues_by_key.get(r.key)]
    jobs = []
    for r in todo:
        members = "\n".join(json.dumps({"id": cid, "statement": cands[cid].statement, "evidence": cands[cid].evidence,
                                        "status": cands[cid].source_status, "doc": cands[cid].doc_id,
                                        "date": cands[cid].doc_date}, ensure_ascii=False)
                            for cid in r.candidate_ids if cid in cands)
        siblings = ", ".join(x.name for x in cons.requirements if x.category == r.category and x.key != r.key)
        content = (f"REQUIREMENT {r.key}: {r.name}\nCategory: {r.category}\nType: {r.type}\n\n"
                   f"SOURCE CANDIDATES:\n{members}\n\nGLOSSARY:\n{glossary}\n\n"
                   f"OTHER REQUIREMENTS IN THIS CATEGORY (do not cover their scope): {siblings or '-'}")
        if issues_by_key.get(r.key):
            content += "\n\nREVIEWER COMMENTS TO ADDRESS:\n" + "\n".join(f"- {i}" for i in issues_by_key[r.key])
        jobs.append([SystemMessage(prompts.clean(prompts.WRITE_SYSTEM)), HumanMessage(content)])

    _log(f"write: {len(todo)} of {len(cons.requirements)} requirements with {config.WRITE_MODEL}")
    results = _llm(config.WRITE_MODEL, WrittenRequirement).batch(
        jobs, config={"max_concurrency": config.WRITE_CONCURRENCY})
    for r, w in zip(todo, results):
        cache[tuple(r.candidate_ids)] = w

    reqs = []
    for r in cons.requirements:
        w = cache[tuple(r.candidate_ids)]
        reqs.append(Requirement(**(r.model_dump() | w.model_dump())))
    spec = Specification(glossary=cons.glossary, requirements=reqs, discarded=cons.discarded)
    return {"written": cache, "spec": spec}


# --- review (LLM) -------------------------------------------------------------

def review(state: GraphState) -> dict:
    content = ("SPECIFICATION:\n" + state["spec"].model_dump_json(indent=1)
               + "\n\nORIGINAL CANDIDATES:\n" + _candidate_lines(state["candidates"], with_source=False)
               + "\n\nAUTOMATIC COVERAGE CHECK:\n" + json.dumps(state["coverage"]))
    _log(f"review: iteration {state['iteration']} with {config.REVIEW_MODEL}")
    result = _llm(config.REVIEW_MODEL, ReviewResult).invoke(
        [SystemMessage(prompts.clean(prompts.REVIEW_SYSTEM)), HumanMessage(content)])
    coverage = state["coverage"]
    score = 2 * len(coverage["missing_candidates"]) + len(coverage["duplicate_names"]) + len(result.issues)
    _log(f"review: approved={result.approved}, issues={len(result.issues)}, score={score} (lower is better)")
    entry = {"iteration": state["iteration"], "approved": result.approved, "coverage_ok": coverage["ok"],
             "missing_candidates": len(coverage["missing_candidates"]), "score": score,
             "issues": [i.model_dump() for i in result.issues]}
    update = {"review": result, "review_log": [entry]}
    best = state.get("best")
    if best is None or score <= best["entry"]["score"]:  # the loop can make things worse; keep the best version
        update["best"] = {"spec": state["spec"], "coverage": coverage, "entry": entry}
    return update


def route_after_review(state: GraphState) -> str:
    """Feedback loop (ANS3): go back to cluster until approved and coverage is clean."""
    done = state["review"].approved and state["coverage"]["ok"]
    if done or state["iteration"] >= state["max_iterations"]:
        return "render"
    return "cluster"


# --- render (deterministic) ------------------------------------------------

_PRIORITY_ORDER = {p: i for i, p in enumerate(prompts.PRIORITY_SCALE)}


def render(state: GraphState) -> dict:
    best = state["best"]
    cons, cands = best["spec"], {c.cid: c for c in state["candidates"]}
    docs = {d.doc_id: d for d in state["documents"]}

    def sources(cids: list[str]) -> list[str]:
        return sorted({cands[c].doc_id for c in cids if c in cands})

    # Deterministic, stable IDs (OS2): sort by category, then priority, then name.
    reqs = sorted(cons.requirements, key=lambda r: (r.category.lower(), _PRIORITY_ORDER[r.priority], r.name.lower()))
    key_to_id = {r.key: f"REQ-{i:03d}" for i, r in enumerate(reqs, 1)}

    def resolve_keys(text: str) -> str:
        return re.sub(r"\bK\d{2,4}\b", lambda m: key_to_id.get(m.group(0), m.group(0)), text)

    cov = best["coverage"]
    lines = [
        "# Software Requirements Specification",
        "",
        f"*Generated {date.today().isoformat()} by the requirements-refinement agentic network "
        f"from `{Path(state['input_dir']).name}` ({len(docs)} source documents, {len(cands)} extracted "
        f"candidate requirements, {state['iteration']} cluster/write/review iteration(s)).*",
        "",
        f"Models: extraction `{config.EXTRACT_MODEL}`, clustering `{config.CLUSTER_MODEL}`, "
        f"writing `{config.WRITE_MODEL}`, review `{config.REVIEW_MODEL}`.",
        "",
        "## Contents",
        "1. Priority scale",
        "2. Glossary",
        "3. Requirements",
        "4. Traceability matrix",
        "5. Discarded requirements (blacklist)",
        "6. Quality assurance log",
        "7. Source documents",
        "",
        "## 1. Priority scale",
        "",
        "Priorities follow the MoSCoW method:",
        "",
        "| Priority | Meaning |",
        "|---|---|",
        *[f"| **{p}** | {m} |" for p, m in prompts.PRIORITY_SCALE.items()],
        "",
        "## 2. Glossary",
        "",
        "The requirements use the following terms consistently. Terms in the last column are avoided.",
        "",
        "| Term | Definition | Avoided synonyms |",
        "|---|---|---|",
        *[f"| {g.term} | {g.definition} | {', '.join(g.avoid) or '-'} |"
          for g in sorted(cons.glossary, key=lambda g: g.term.lower())],
        "",
        "## 3. Requirements",
        "",
        "| Priority | Count |",
        "|---|---|",
        *[f"| {p} | {sum(r.priority == p for r in reqs)} |" for p in prompts.PRIORITY_SCALE],
        f"| **Total** | **{len(reqs)}** |",
    ]
    current_category, category_no = None, 0
    for r in reqs:
        if r.category != current_category:
            current_category, category_no = r.category, category_no + 1
            lines += ["", f"### 3.{category_no} {r.category}"]
        rid = key_to_id[r.key]
        lines += [
            "",
            f"#### {rid}: {r.name}",
            "",
            f"- **Type:** {r.type}",
            f"- **Priority:** {r.priority} — {r.priority_rationale}",
            f"- **Sources:** {', '.join(f'`{s}`' for s in sources(r.candidate_ids))}",
            f"- **Derived from candidates:** {', '.join(r.candidate_ids)}",
            "",
            resolve_keys(r.description),
        ]

    lines += ["", "## 4. Traceability matrix", "", "| Source document | Requirements | Discarded |", "|---|---|---|"]
    by_doc, disc_by_doc = defaultdict(set), defaultdict(set)
    for r in reqs:
        for s in sources(r.candidate_ids):
            by_doc[s].add(key_to_id[r.key])
    for i, d in enumerate(cons.discarded, 1):
        for s in sources(d.candidate_ids):
            disc_by_doc[s].add(f"DIS-{i:03d}")
    for doc_id in sorted(docs):
        lines.append(f"| `{doc_id}` | {', '.join(sorted(by_doc[doc_id])) or '-'} | "
                     f"{', '.join(sorted(disc_by_doc[doc_id])) or '-'} |")

    lines += ["", "## 5. Discarded requirements (blacklist)", "",
              "Requirements identified in the sources but not included in the specification.", ""]
    if not cons.discarded:
        lines.append("*No requirements were discarded.*")
    for i, d in enumerate(cons.discarded, 1):
        lines += [
            f"#### DIS-{i:03d}: {d.name}",
            "",
            f"- **Reason:** {d.reason_category}",
            f"- **Sources:** {', '.join(f'`{s}`' for s in sources(d.candidate_ids))}",
            f"- **Candidates:** {', '.join(d.candidate_ids)}",
            "",
            resolve_keys(d.explanation),
            "",
        ]

    lines += ["", "## 6. Quality assurance log", "",
              f"Each iteration is scored (2 × missing candidates + duplicate names + reviewer issues); this "
              f"document is the version from iteration **{best['entry']['iteration']}**, which scored best.", "",
              "| Iteration | Reviewer approved | Missing candidates | Reviewer issues | Score |",
              "|---|---|---|---|---|"]
    for e in state["review_log"]:
        lines.append(f"| {e['iteration']} | {'yes' if e['approved'] else 'no'} | {e['missing_candidates']} | "
                     f"{len(e['issues'])} | {e['score']} |")
    open_issues = best["entry"]["issues"]
    if open_issues:
        lines += ["", "**Open reviewer issues for this version (not resolved within the iteration limit):**", ""]
        lines += [f"- *{i['kind']}* ({resolve_keys(', '.join(i['keys']))}): {resolve_keys(i['description'])}"
                  for i in open_issues]
    if not cov["ok"]:
        lines += ["", "**Automatic coverage check findings for this version:**", ""]
        lines += [f"- {k}: {', '.join(map(str, v))}" for k, v in cov.items()
                  if k not in ("ok", "auto_repaired") and v]
        for cid in cov["missing_candidates"]:
            c = cands[cid]
            lines.append(f"  - {cid} (`{c.doc_id}`): {c.title}: {c.statement}")

    lines += ["", "## 7. Source documents", "", "| Document | Kind | Date | Candidates extracted |", "|---|---|---|---|"]
    per_doc = Counter(c.doc_id for c in cands.values())
    for doc_id, d in sorted(docs.items()):
        lines.append(f"| `{doc_id}` | {d.kind} | {d.date or '-'} | {per_doc[doc_id]} |")

    _log(f"render: {len(reqs)} requirements, {len(cons.discarded)} discarded")
    return {"document": "\n".join(lines) + "\n"}
