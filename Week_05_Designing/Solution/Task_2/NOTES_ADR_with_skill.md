# NOTES_ADR – zmeny ADR pre CDC Shop

Change log k [ADR.md](ADR.md): každá pripomienka používateľa, čo sa zmenilo a prečo.

## v1 – 2026-11-01
- **Vytvorené:** ADR log s registrom, ADR-001 (štýl architektúry: modulárny monolit + worker) a ADR-002 (platobný tok a stavový automat objednávky). Plánované ADR-003 až ADR-005.
- **Predvolené voľby (používateľ ich zatiaľ nepotvrdil):** angličtina, jeden súbor, MADR shortened, status `Proposed`.
- **Kontrola podľa quality-checklist.md:**
  - váhy = 100 %, tabuľka, scenáre aj break-even skopírované z výstupu `weighted_score.py` ([drivers.json](drivers.json));
  - pravidlo „externé systémy volá len worker, okrem vytvorenia platobnej session“ je rovnaké v pravidlách, diagrame, allowliste arch. testov aj v ADR-002;
  - stavy v stavovom diagrame zodpovedajú textu ADR-002;
  - otvorené otázky v ADR zodpovedajú [NOTES.md §4](NOTES.md);
  - Mermaid syntax skontrolovaná ručne – vykreslenie neoverené (treba skontrolovať v Markdown preview).
