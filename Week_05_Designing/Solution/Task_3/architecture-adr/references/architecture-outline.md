# NOTES.md template and architecture outline

## NOTES.md template

Write it in the agreed notes language. Keep the four numbered sections stable; the log grows.

```markdown
# NOTES – Architectures for <System>

Running notes from the architecture discussion. Not a transcript – the state of knowledge after each exchange.
Requirements: [<file>](<path>)

## Session metrics
| Metric | Value |
|---|---|
| Start / end | <YYYY-MM-DD HH:MM> / – |
| User questions (Task 1) | 0 |
| Corrections I made | 0 |
| User change requests (Task 2) | 0 |
| ADR versions | 0 |

---

## 1. System summary
**What it is:** <one paragraph>

**Roles:**
| Role | What it does |
|---|---|

**Functional areas (bounded contexts):**
- **<Area>** – <capabilities> (US x, y, z)

**Non-functional requirements (derived – not in the spec):**
- *Hygiene (do not decide the choice):* …
- *Deciding:* …

**Ambiguities and gaps (by architectural impact):**
1. …

**Working assumptions (to be confirmed):** load …, peak …, data size …, team …, availability …, latency …

---

## 2. Three proposed architectures
### A) <name>
<outline below>
### B) <name>
### C) <name>
### Essential vs. accidental complexity

---

## 3. Discussion log
- **<date> – start:** …
- **Question 1 – <topic>:** …

## 4. Open questions / decisions
- [ ] …
- [x] … → **<answer>**, confirmed by <user> on <date>
```

## Outline of one architecture

Use these headings for every option so they can be compared line by line.

- **Components:** clients → entry point → business components → data stores → external systems.
- **Communication:** sync vs. async, in-process vs. network, which flows use which.
- **Key mechanisms:** the techniques the option relies on (state machine, outbox, saga, idempotent handlers, CDN cache, read model…).
- **+ Pros:** 3–5 bullets tied to this system, not generic marketing.
- **– Cons:** 3–5 bullets.
- **Hardest to implement:** concrete problems with user-story references (e.g. "payment outside our transaction – US 7").
- **When to choose it:** team size, load profile, organisation, constraints.
- **Minimal reasonable version:** the smallest variant that still deserves the name (e.g. 3 services with own DBs, not 10 services on one DB).
- **Diagram:** Mermaid `flowchart` with external systems dashed (`classDef external stroke-dasharray: 5 5`).

## Quality examples (CDC Shop – reuse the depth, not the conclusions)

**System summary excerpt**

> **Functional areas:** Identity – registration, login, logout, profile (US 1, 2, 3, 8, 13, 14, 19) · Catalog – list, detail, search by name, sort by price (US 5, 6, 11, 12, 17, 18, 21, 22) · …
>
> **Hygiene NFRs:** card data never stored (hosted payment page, PCI SAQ-A), password hashing, RBAC, GDPR – all three options meet them the same way.
> **Deciding NFRs:** operability for a 2–4 person team, load profile, failure isolation, payment consistency, cost, lock-in.
>
> **Ambiguities:** 1. one shop or a marketplace? (changes product ownership and payments) 2. inventory not mentioned 3. nobody on the merchant side sees or ships orders, yet US 9 shows shipment status …

**Architecture excerpt**

> **A) Modular monolith** – *Components:* SPA → one backend (modules Identity, Catalog, Cart, Ordering, Payment, Shipping, Contact) → one PostgreSQL (schema per module) → gateway (webhooks), carrier API, SMTP. *Communication:* in-process facades and domain events, no foreign tables. *Key mechanisms:* order state machine, idempotent webhook handler, price snapshot in order lines, trigram search. *Hardest:* payment outside the DB transaction (webhooks, idempotency, reconciliation), keeping module boundaries, search with diacritics. *When:* 1–6 developers, one shop, MVP, moderate load. *Minimal version:* the same; the useful extension is A′ = + worker process + job queue for external calls.

**Insights that changed the outcome in that run** (look for their equivalents):
- Scope questions (marketplace? inventory?) removed whole services and most of the saga.
- "Monolith" (deployment granularity) and "distributed" (nodes communicating over a network) are independent axes.
- The minimal microservices variant turned out to be the monolith after two module extractions – compare minimal versions, not only full ones.
- Infrastructure cost was noise; people and payment fees dominated. Always estimate people, not only cloud bills.
