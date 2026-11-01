# Deep-dive question catalog

Generalised from the questions the user asked in the earlier run. Offer the relevant ones as a menu after
presenting the three options (Phase 3). For each, the answer must contain the listed elements.

## Scope and requirements

| # | Question | A good answer contains |
|---|---|---|
| 1 | **Scope:** single tenant or multi-tenant/marketplace? Inventory? Guest users? | Consequences for **each** option (what disappears, what becomes simpler), risk accepted by the simplification, cheap future-proofing. |
| 2 | **Where do the NFRs come from, and which one decides?** | Admit which are derived. Hygiene vs. deciding split. Ranking of deciding drivers. Working assumptions as numbers awaiting confirmation. |
| 3 | **Does option X contradict the spec** (e.g. "distributed system" vs. monolith)? | Definitions of both terms; whether they are independent axes; the strict and loose interpretation; a compromise variant; the anti-pattern to avoid (distributed monolith); an open question for the client. |

## Understanding an option

| # | Question | A good answer contains |
|---|---|---|
| 4 | **Explain a concept** the option relies on (modular vs. plain monolith, architecture tests, idempotency, outbox…). | Definition, example from **this** system, what breaks without it, the cost, tools per ecosystem, limits of the technique. |
| 5 | **Draw the critical flow's state machine.** | Mermaid `stateDiagram-v2`; table transition → trigger → when; races (e.g. late payment) and the rule that resolves them (source of truth); what is *not* a state; implementation rules (conditional update, transition history); gaps in the spec. |
| 6 | **Variants inside an option** (choreography vs. orchestration, DynamoDB vs. relational, sync vs. async…). | Comparison table on coupling, visibility, change, timeouts/compensation, risk; recommendation for this system; a hybrid if justified; painful parts of each. |
| 7 | **Minimal reasonable version** of an option. | What defines the style (not the number of components); merge/split principle; concrete minimal set with communication; which hard problems disappear; honest comparison with the other options; fixed platform costs that do not shrink. |

## Operations and evolution

| # | Question | A good answer contains |
|---|---|---|
| 8 | **When does the chosen option stop being enough, and what is extracted first?** | Cheap steps first; measurable signals; prerequisites (stable boundary); bad reasons; ordered extraction candidates with risk; migration pattern (strangler fig); metrics to prepare now. |
| 9 | **Debug a production incident** (e.g. "customer paid, order cancelled"). | Hypotheses ordered by likelihood; step-by-step procedure along the identifiers; how to fix for the customer (audited command, never a manual UPDATE); design-for-debuggability conclusions; comparison across options. |
| 10 | **Platform pain points** (cold start, hot partition, connection storms, limits…). | Mechanism explained; typical numbers; impact per path in this system; whether it matters at the assumed load; mitigations ordered by effectiveness with their costs; what to measure. |
| 11 | **Vendor lock-in and migration cost.** | Lock-in = cost of leaving; table component → lock-in level → what migration means → estimate; hidden costs; total in person-weeks compared with other options; how likely leaving is; strategy (accept where it pays, avoid where it does not); no multi-cloud abstraction layers. |
| 12 | **Local development and testing.** | Table area → locally? → how → fidelity; what only works in the cloud; recommended strategy (ephemeral stacks, test pyramid); interaction with other choices (e.g. DB cost per stack); comparison across options. |

## Synthesis

| # | Question | A good answer contains |
|---|---|---|
| 13 | **Shared vs. option-specific problems.** | Essential vs. accidental complexity (Brooks); list per option with a one-word verdict (few / medium / most). |
| 14 | **Cost and people at two volumes** (current and 100×). | Explicit assumptions block (order value, conversion, FTE cost…); orders → requests per second (usually tiny); build cost in person-months; infra per month; people per month; total; context (payment fees, margin) – infra is often noise. Mark everything as order-of-magnitude. |
| 15 | **Which option and why?** | Leads into Phase 4: weighted table from the script, sensitivity, break-even, then ask the user to decide. |
