"""Model assignment per LLM node (ANS4: three different models). Override via environment variables."""

import os

EXTRACT_MODEL = os.getenv("EXTRACT_MODEL", "gpt-5-mini")          # many cheap per-document calls
CLUSTER_MODEL = os.getenv("CLUSTER_MODEL", "gpt-6-luna")          # hardest reasoning step, one big call
WRITE_MODEL = os.getenv("WRITE_MODEL", "gpt-5.4-nano")            # many small, well-scoped writing calls
REVIEW_MODEL = os.getenv("REVIEW_MODEL", "gpt-5.6-luna")          # independent critic, different model

SUPPORTED_EXTENSIONS = {".txt", ".md", ".eml"}
CHUNK_CHARS = 20_000         # longer documents are split so extraction stays exhaustive
EXTRACT_CONCURRENCY = 6
WRITE_CONCURRENCY = 10
LLM_TIMEOUT_S = 900
