"""Run the requirements-refinement network on a directory of input documents.

Usage:
    python main.py --input data/corpus --output output/requirements.md
"""

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from graph import build_graph  # noqa: E402  (config reads env vars at import time)
from schemas import Candidate  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="Directory with the input corpus (searched recursively).")
    parser.add_argument("--output", default="output/requirements.md", help="Path of the generated Markdown document.")
    parser.add_argument("--max-iterations", type=int, default=3, help="Maximum cluster/write/review rounds.")
    parser.add_argument("--reuse-candidates", help="candidates.json from an earlier run on the same input; "
                                                   "skips the extraction LLM calls (for debugging).")
    args = parser.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    graph = build_graph()
    (out.parent / "graph.mmd").write_text(graph.get_graph().draw_mermaid(), encoding="utf-8")

    initial = {"input_dir": args.input, "max_iterations": args.max_iterations}
    if args.reuse_candidates:
        initial["candidates"] = [Candidate(**c) for c in
                                 json.loads(Path(args.reuse_candidates).read_text(encoding="utf-8"))]
    state = graph.invoke(initial, config={"recursion_limit": 10 + 4 * args.max_iterations})

    out.write_text(state["document"], encoding="utf-8")
    # Intermediate artifacts for debugging and for the report.
    (out.parent / "candidates.json").write_text(
        json.dumps([c.model_dump() for c in state["candidates"]], indent=1, ensure_ascii=False), encoding="utf-8")
    (out.parent / "specification.json").write_text(state["best"]["spec"].model_dump_json(indent=1), encoding="utf-8")
    (out.parent / "review_log.json").write_text(
        json.dumps(state["review_log"], indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Written {out} (+ graph.mmd, candidates.json, specification.json, review_log.json)")


if __name__ == "__main__":
    main()
