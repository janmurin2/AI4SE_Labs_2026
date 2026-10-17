# Task 2 – Porovnanie promptov

Model **gpt-5.6-luna Efficiency** vytvoril SQL dotazy pre 155 otázok z `restaurants_questions.csv`. Každý z troch promptov z Task 1 bežal v novej relácii a výsledok vyhodnotil skript `evaluate_retrieval_predictions.py`.


| Prompt   | Správne  | Presnosť | Čas inferencie | Čas / otázka |
| -------- | --------- | --------- | --------------- | -------------- |
| ICIO     | 146 / 155 | 94,19 %   | 31 min 32 s     | 12,2 s         |
| Few-Shot | 155 / 155 | 100,00 %* | 24 min 51 s     | 9,6 s          |
| GKP      | 142 / 155 | 91,61 %   | 33 min 15 s     | 12,9 s         |

**Few-Shot** bol najpresnejší aj najrýchlejší: ukážky SQL zjavne pomohli najviac. **ICIO** skončil druhý. **GKP** bol najhorší v presnosti aj čase, keďže vlastné odvodenie šablón predĺžilo beh a nezlepšilo výsledok.

\* Výsledok Few-Shot je nadhodnotený. Pri otázkach s prázdnym výsledkom agent niekedy vrátil `WHERE 1 = 0`, čo otázku nerieši, len trafí očakávaný prázdny výstup. Agenti mali prístup k celému priečinku projektu vrátane správnych výsledkov, takže podobné správanie sa nedá vylúčiť ani pri ostatných promptoch.
