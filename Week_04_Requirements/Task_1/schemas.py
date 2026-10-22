"""Data models shared by the nodes of the requirements-refinement network."""

from typing import Literal

from pydantic import BaseModel, Field

RequirementType = Literal["functional", "non-functional", "constraint", "documentation", "assumption"]
Priority = Literal["Must", "Should", "Could", "Won't"]


# --- Corpus ---------------------------------------------------------------

class SourceDocument(BaseModel):
    doc_id: str = Field(description="Relative path of the file inside the corpus directory.")
    kind: str = Field(description="email, meeting minutes, interview, specification, ...")
    date: str | None = Field(default=None, description="ISO date if it could be determined.")
    text: str


# --- Extraction (one LLM call per document) --------------------------------

class ExtractedRequirement(BaseModel):
    title: str = Field(description="Short descriptive name, 3-8 words.")
    statement: str = Field(description="The requirement as one clear 'The system shall ...' sentence.")
    type: RequirementType
    source_status: Literal["proposed", "agreed", "rejected", "deferred", "questioned"] = Field(
        description="How the source document treats this requirement (e.g. 'rejected' if a meeting "
                    "explicitly decided against it, 'questioned' if raised as an open question).")
    evidence: str = Field(description="Short verbatim quote from the document supporting the requirement.")


class ExtractionResult(BaseModel):
    requirements: list[ExtractedRequirement]


class Candidate(ExtractedRequirement):
    """An extracted requirement after the deterministic tagging with ID and source."""
    cid: str
    doc_id: str
    doc_date: str | None = None


# --- Clustering (LLM): structure of the specification --------------------------

class RequirementCluster(BaseModel):
    key: str = Field(description="Stable temporary key, e.g. 'K001'. Keep keys stable between revisions.")
    name: str = Field(description="Short descriptive name, 3-8 words, using glossary vocabulary.")
    category: str = Field(description="Functional area, e.g. 'Circulation', 'Cataloging', 'Reporting', "
                                      "'Security & Access', 'Operating Environment'.")
    type: RequirementType
    candidate_ids: list[str] = Field(description="IDs (C-xxx) of ALL extracted candidates merged into this requirement.")


class DiscardedRequirement(BaseModel):
    name: str
    reason_category: Literal["conflicting", "rejected-by-stakeholders", "nonsensical", "out-of-scope", "superseded"]
    explanation: str = Field(description="Why it was discarded; name the requirement key it conflicts with if any.")
    candidate_ids: list[str]


class GlossaryTerm(BaseModel):
    term: str
    definition: str
    avoid: list[str] = Field(description="Synonyms that must NOT be used in requirements (may be empty).")


class ClusteringResult(BaseModel):
    glossary: list[GlossaryTerm]
    requirements: list[RequirementCluster]
    discarded: list[DiscardedRequirement]


class ClusterPatch(BaseModel):
    """Revision of a previous ClusteringResult; applied deterministically so untouched parts cannot be lost."""
    upserts: list[RequirementCluster] = Field(
        description="Requirements to add or replace (matched by key), each with its COMPLETE candidate_ids list. "
                    "Candidate IDs listed here are automatically removed from all other requirements.")
    removed_keys: list[str] = Field(description="Keys of requirements to delete (e.g. after merging them into another).")
    glossary: list[GlossaryTerm] = Field(description="The complete, revised glossary.")
    discarded: list[DiscardedRequirement] = Field(description="The complete, revised list of discarded requirements.")


# --- Writing (LLM, one call per cluster) --------------------------------------

class WrittenRequirement(BaseModel):
    name: str = Field(description="Short descriptive name, 3-8 words (may refine the proposed name).")
    description: str = Field(description="One paragraph (3-6 sentences): what the system shall do, "
                                         "details/conditions, and the rationale / who needs it.")
    priority: Priority
    priority_rationale: str = Field(description="One sentence justifying the priority.")


class Requirement(RequirementCluster, WrittenRequirement):
    """Cluster + written text, assembled deterministically."""


class Specification(BaseModel):
    glossary: list[GlossaryTerm]
    requirements: list[Requirement]
    discarded: list[DiscardedRequirement]


# --- Review (LLM) ----------------------------------------------------------

class ReviewIssue(BaseModel):
    kind: Literal["duplicate", "conflict", "vocabulary", "missing", "priority", "quality", "traceability"]
    keys: list[str] = Field(description="Affected requirement keys and/or candidate IDs.")
    description: str
    suggested_fix: str


class ReviewResult(BaseModel):
    approved: bool = Field(description="True only if no significant issue remains.")
    issues: list[ReviewIssue]
