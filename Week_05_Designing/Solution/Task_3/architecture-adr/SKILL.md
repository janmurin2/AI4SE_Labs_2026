---
name: architecture-adr
description: Propose and compare software architectures from a requirements document, then choose one and write Architecture Decision Records (ADRs). Use when the user wants to read requirements (user stories, a spec, a /data file), propose several distinct architectures (e.g. modular monolith, microservices, serverless), discuss their trade-offs and painful implementation details, pick one, and record the decision as an ADR. Triggers - "propose an architecture", "compare architectures", "architecture options", "ADR", "architecture decision record", "navrhni architektúru", Week_05 Task 1 / Task 2.
---

# Architecture proposals and ADRs

This skill covers the full path from requirements to a reviewed ADR:
**setup → system summary → 3 distinct architectures → discussion → closing the choice → ADR → quality check.**

It encodes what worked in an earlier run (CDC Shop, Week_05) and front-loads everything the user
had to ask for or correct there. Do the things marked **(from the start)** in the first version,
not after the user asks.

Supporting files (read them when the phase says so, not upfront):
- [references/architecture-outline.md](references/architecture-outline.md) – NOTES.md template, per-architecture outline, quality examples
- [references/question-catalog.md](references/question-catalog.md) – deep-dive questions and what a good answer must contain
- [references/adr-template.md](references/adr-template.md) – ADR log template (final structure from the earlier run)
- [references/quality-checklist.md](references/quality-checklist.md) – checks before handing an ADR over
- [scripts/weighted_score.py](scripts/weighted_score.py) – weighted scores, sensitivity analysis, break-even points

## Ground rules

- **Notes are mandatory and continuous.** Write the notes file before the first answer and update it after
  every substantive exchange. It records the current state of knowledge, not a transcript.
- **Never present derived facts as given.** Non-functional requirements, load, team size and budgets are almost
  never in the spec. Label them *derived* until the user confirms them; record the confirmation with a date.
- **Never compute numbers by hand** for weighted scores or sensitivity. Use the script and paste its output.
- **Correct yourself openly.** When an earlier proposal was wrong, write `Correction:` in the notes with the reason.
- **Do not reuse the earlier system's answers.** The examples in the references come from CDC Shop (a small
  e-shop). Reuse the *method*, not the conclusions; a different system may well need microservices or serverless.
- Ask questions in batches with a proposed default for each, so the user can answer "yes" to all.

## Phase 0 – Setup (before anything else)

1. Locate the requirements file and the task files. Read the task assignment if one exists.
2. Create `NOTES.md` next to the task files using the template in `architecture-outline.md`. Fill in the
   **Session metrics** block (start time, counters at 0). Increment counters as you go:
   user questions, corrections you made, user change requests, ADR versions.
3. Ask **one** setup question with defaults:
   - ADR language – default **English**; notes language – default **the user's language**.
   - Output layout – default **one `ADR.md` file containing an ADR log** (register + one section per ADR).
   - Template – default **MADR (shortened)**.

## Phase 1 – Read requirements, summarize the system

Read the whole requirements file. Write section 1 of NOTES.md:
- **Roles** (table: role → what it does), including implicit external systems (payment, carrier, e-mail…).
- **Functional areas / bounded contexts**, each with the user-story IDs it covers. Every story must map somewhere.
- **Non-functional requirements**, explicitly marked as *derived*, split into:
  - *hygiene* – every architecture meets them the same way (PCI via hosted payment page, password hashing, RBAC, GDPR) → they do not decide the choice;
  - *deciding* – where architectures differ (operability vs. team size, load profile and scalability, failure isolation, consistency, cost, lock-in).
- **Ambiguities and gaps**, ordered by architectural impact (e.g. single tenant vs. marketplace, inventory,
  missing stories for one role, guest checkout, deletion of referenced data).
- **Working assumptions as numbers**: load (per month and peak), data size, team size and ops capacity,
  availability, latency target.

Then ask the user about the **3–5 highest-impact ambiguities and the working assumptions** in one message.
Record each answer in the discussion log with its consequences for every architecture.

## Phase 2 – Three distinct architectures

The three options must differ on real axes, not be three flavours of one idea:
- deployment granularity (one deployable vs. independent services),
- operations model (self-run vs. managed vs. serverless/BaaS),
- consistency model (local ACID vs. sagas / eventual consistency).

A typical good set: **modular monolith (+ async worker)**, **microservices + events/saga**, **serverless /
managed services**. Use others (event sourcing + CQRS, service-based, space-based, hexagonal on PaaS…) when the
requirements push that way. If a fitting option is unknown, name well-known architectures and evaluate them.

For **each** architecture use the outline from `architecture-outline.md`:
components · communication · key mechanisms · pros · cons · **hardest implementation parts** (concrete, tied to
user stories) · when to choose it · **minimal reasonable version** · one Mermaid diagram.

Close the section with a short **essential vs. accidental complexity** split: problems every option has
(from the domain) vs. problems a specific option adds. State your default recommendation and why, but do not
treat it as decided.

## Phase 3 – Discussion loop

After presenting the options, offer a short menu (5–8 items) of deep dives from `question-catalog.md`
that fit this system – e.g. contradiction with the spec, the critical flow's state machine, debugging a
production incident, when the chosen style stops being enough, lock-in and migration cost, local development,
cost and people at two volumes. The user may pick or ask anything else.

For every exchange:
- answer with the elements the catalog lists for that question type (tables and Mermaid diagrams where they help);
- add a log entry `**Question N – <topic>:**` with the conclusions, not the conversation;
- update sections 1–2 of NOTES.md if the answer changed an option (e.g. a removed state, a different database);
- move answered items in **Open questions** to `[x]` with the answer.

## Phase 4 – Close the choice (bridge between Task 1 and Task 2)

Do not start the ADR while the choice is implicit.
1. Build the decision-driver table: 4–7 drivers taken from the *deciding* NFRs, a weight per driver with a
   one-line justification, scores 1–5 per option. Write it as JSON and run
   `python .claude/skills/architecture-adr/scripts/weighted_score.py <file.json>` (see the script header for the format).
2. Ask the user in one message to: (a) choose the architecture, (b) confirm the working assumptions,
   (c) decide how each remaining open question is handled in the ADR (decided / open question / out of scope).
3. Record the answers in NOTES.md **Open questions** as `[x] … → confirmed by <user> on <date>`.
   This is the trace that the ADR's "Confirmed assumptions" will point to.

## Phase 5 – Write the ADR

1. Create `NOTES_ADR.md` (change log of the ADR: each user remark, what changed, why).
2. Read `adr-template.md` and write the ADR log in the agreed language and layout.
3. **(from the start)** rules that caused most rework in the earlier run:
   - **One ADR = one decision.** ADR-001 is the architecture style. Sub-decisions that have their own
     alternatives (job queue, payment flow, identity/sessions, search, stack…) become ADR-002+ when they carry
     a main risk, otherwise they are listed as *Planned* in the register. Domain rules (soft delete, price
     snapshot…) are not ADRs – they go to NOTES or a design document.
   - **Length 1–2 pages per ADR.** Context refers to the requirements instead of copying story tables;
     NFRs fit in one paragraph; risks are the top 3.
   - **Summary of 3–4 sentences** under the metadata: decision, main reason, main price, main open question.
   - **Weighted table + sensitivity analysis + break-even** pasted from the script output, with the method
     stated (one weight changes, the others are rescaled proportionally) and every scenario's weights shown.
   - **Mermaid diagrams**: component flowchart in ADR-001 (external systems dashed, arrows that match the
     rules); a sequence diagram per critical flow (separate diagrams for the happy path and the
     failure/recovery path rather than one diagram with nested `alt`); a state diagram for the main entity.
   - **Confirmation section**: how compliance is checked (architecture tests, DB permissions, metrics,
     review dates) and when to revisit (measurable signals).
   - **Status `Proposed`** while open questions remain.
4. Present the ADR with a 3–5 line summary of what each record contains and which defaults you chose.
5. For each user remark: log it in NOTES_ADR.md, apply it to **all** affected records (cross-references,
   anchors, repeated rules), increment the counters.

## Phase 6 – Quality check and handover

Before every handover of an ADR version, go through `quality-checklist.md` and fix what fails.
Tell the user in 2–4 lines what you checked and anything you could not verify (e.g. Mermaid rendering
without a renderer – ask them to check the Markdown preview).

At the end of the session, fill the **Session metrics** block in NOTES.md (end time, counters, number of ADR
versions) – it is the input for comparing runs with and without this skill.
