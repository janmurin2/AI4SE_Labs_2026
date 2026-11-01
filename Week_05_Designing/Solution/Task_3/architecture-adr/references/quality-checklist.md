# ADR quality checklist

Run before every handover of an ADR version. Each item came from a real correction in the earlier run.

## Structure and scope
- [ ] Template is named in the file header (MADR shortened) and section names follow it.
- [ ] Register at the top lists every record (ID, decision, status, one sentence) and *Planned* ones.
- [ ] **One ADR = one decision.** No record contains nested decisions that have their own alternatives.
- [ ] Each ADR is **≤ 2 pages**. No copied story tables, full risk registers or domain rules.
- [ ] Each ADR has a **3–4 sentence summary**: decision, main reason, main price, main open question.
- [ ] Status is `Proposed` while open questions remain; `Accepted` only after the user says so.
- [ ] Language matches the agreed one in all records and file names.

## Numbers and claims
- [ ] Weights add up to 100% and each has a justification.
- [ ] Weighted scores, sensitivity scenarios and break-even points are **pasted from `weighted_score.py`**, not computed by hand.
- [ ] The sensitivity method is stated and every scenario shows its full weight vector.
- [ ] **Every number in the ADR can be derived from data stated in the ADR** or a linked source.
- [ ] Cost figures are labelled as order-of-magnitude estimates with their key assumption (e.g. FTE cost).
- [ ] Every "confirmed" assumption has a trace in NOTES.md (who, when) and the ADR says the spec does not contain it.

## Consistency
- [ ] **Every rule with an exception has a confirmation test with the same allowlist** (e.g. "only the worker calls external systems, except creating the payment session" ↔ arch test allowlist).
- [ ] Diagram arrows match the written rules (no arrow the rules forbid, no allowed flow missing).
- [ ] Repeated statements (rules, allowlists, state names) are identical across records, or one record links to the other.
- [ ] Cross-references use in-file anchors (`<a id="adr-001"></a>`) and every link resolves.
- [ ] Open questions in the ADR match the open items in NOTES.md.
- [ ] Nothing the user removed from the notes was reintroduced; if it is relevant, ask instead.

## Diagrams
- [ ] Mermaid, not ASCII.
- [ ] ADR-001: component `flowchart`, external systems dashed, legend line below.
- [ ] Critical flow: `sequenceDiagram` – happy path and failure/recovery path as separate diagrams.
- [ ] Main entity: `stateDiagram-v2` with the trigger on every transition.
- [ ] Mermaid syntax checked (quoted labels with special characters, `<br/>` for line breaks). If no renderer is available, tell the user to check the preview.

## Decision quality
- [ ] Every considered option has its strongest argument stated fairly (no strawmen).
- [ ] The Confirmation section says how compliance is verified (tests, permissions, metrics) and when the ADR is reviewed.
- [ ] "Revisit when" lists measurable signals, not opinions.
- [ ] The way out (how to move to another option later) is stated.
