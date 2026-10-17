# Task 1 – Prompty pre Text-to-SQL (reštaurácie), dávkový režim

Tri prompty pre Task 2, každý podľa iného frameworku z [frompting.com/frameworks](https://frompting.com/frameworks). Každý prompt spracuje **všetkých 155 otázok naraz** zo súboru `restaurants_questions.csv` a vytvorí súbor `restaurants_dataset_predictions.csv`, ktorý priamo načíta `evaluate_retrieval_predictions.py`.

## Ako prompt použiť

1. Otvor v Copilote nový chat (pre každý prompt samostatne).
2. Prilož súbor `restaurants_questions.csv`.
3. Skopíruj celý text promptu z bloku nižšie a odošli ho. Nič v ňom netreba dopĺňať.
4. Stiahni súbor `restaurants_dataset_predictions.csv`. Ak ho Copilot nevytvorí ako súbor, ulož pod týmto názvom obsah bloku `csv` z odpovede.
5. Súbor vlož do priečinka so skriptom a spusti `python evaluate_retrieval_predictions.py`.

Modelu nedávaj `restaurants_dataset.csv`, lebo obsahuje aj správne výsledky (stĺpec `result`).

## Formát výstupu

```csv
question,predicted_sql
"what is the best thai in the bay area ?","SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME FROM ... WHERE ..."
```

Otázka musí byť zhodná so vstupom znak po znaku, lebo podľa nej skript páruje správny výsledok. Formát som overil spustením skriptu na súbore v tomto tvare so všetkými 155 otázkami.

## Prehľad

| ID | Framework | Zdroj | Technika |
| --- | --- | --- | --- |
| P1_ICIO | ICIO (Instruction-Context-Input-Output) | [frompting.com/frameworks/icio](https://frompting.com/frameworks/icio) | structured instruction (no examples, no reasoning) |
| P2_FEWSHOT | Few-Shot Learning | [frompting.com/frameworks/few-shot](https://frompting.com/frameworks/few-shot) | in-context examples (6 example rows of the input and output CSV, not taken from the test set) |
| P3_GKP | GKP (Generate-Knowledge-Prompting) | [frompting.com/frameworks/gkp](https://frompting.com/frameworks/gkp) | two phases: generate knowledge (question types, SQL templates, pitfalls), then answer from it |

## P1_ICIO – ICIO (Instruction-Context-Input-Output)

Zdroj: https://frompting.com/frameworks/icio

````text
# INSTRUCTION
For every question in the input, write one SQLite SELECT query that retrieves the restaurants the question asks for.
Process all questions in one pass and return the result as a single CSV file.

# CONTEXT
You are working with a restaurant guide database for California.
Database: SQLite.
Tables and columns:
  RESTAURANT(ID INTEGER PRIMARY KEY, NAME TEXT, FOOD_TYPE TEXT, CITY_NAME TEXT, RATING REAL)
  LOCATION(RESTAURANT_ID INTEGER PRIMARY KEY -> RESTAURANT.ID, HOUSE_NUMBER INTEGER, STREET_NAME TEXT, CITY_NAME TEXT)
  GEOGRAPHIC(CITY_NAME TEXT PRIMARY KEY, COUNTY TEXT, REGION TEXT)
All text values are lowercase (e.g. 'san francisco', 'italian', 'bay area').
Known REGION values: 'bay area', 'napa valley', 'monterey', 'lake tahoe', 'sacramento area',
'los angeles area', 'yosemite and mono lake area', 'northern california', 'unknown'.

Conventions used by this database (follow them exactly, the answers are graded by comparing returned rows):
1. Always return exactly two columns: SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME,
   from RESTAURANT JOIN LOCATION ON RESTAURANT.ID = LOCATION.RESTAURANT_ID. Never use DISTINCT, ORDER BY or LIMIT.
2. A city ("in <city>") filters LOCATION.CITY_NAME.
3. A region ("in the <region>", e.g. "the bay area") joins GEOGRAPHIC ON RESTAURANT.CITY_NAME = GEOGRAPHIC.CITY_NAME
   and filters GEOGRAPHIC.REGION.
4. A street ("on <street>") filters LOCATION.STREET_NAME with = and the street text exactly as written.
5. A cuisine or kind of food ("mexican food", "a pizza restaurant", "places for chinese") filters RESTAURANT.FOOD_TYPE.
6. A restaurant name ("where is <name> in <city>") filters RESTAURANT.NAME.
7. "rating above X" means RESTAURANT.RATING > X. The text in parentheses ("good or better") is only a label; ignore it.
8. "the best ..." means RESTAURANT.RATING = (SELECT MAX(RATING) ...) computed in a subquery with the same filters.
9. Copy literal values exactly as they appear in the question (lowercase, keep abbreviations like "st", "ave", "blvd").
10. Ignore every sentence that is not part of the restaurant request (musings about pasta, pancakes, picnics ...).
    Such noise must never become a filter.
11. Inside SQL use single quotes for text values; an apostrophe inside a value is doubled ('bette''s oceanview diner').
    Never use double quotes inside the SQL.

# INPUT
The input is the attached file restaurants_questions.csv (header: question), one question per row, 155 rows in total.
Read the whole file; do not skip any row.
It contains only the questions, not the expected answers. Some questions contain unrelated sentences (noise).

# OUTPUT
The output is the content of the file restaurants_dataset_predictions.csv:
- UTF-8 CSV, comma-separated, first line is exactly the header: question,predicted_sql
- exactly one row per input question, in the same order as the input, no row skipped, merged or added
- column question: the question copied character for character from the input (including noise, commas,
  spaces before "?" and capitalisation); the file is matched to the answers by this exact text
- column predicted_sql: one SQLite query on a single line, no line breaks, no trailing semicolon
- every value in the data rows (question, predicted_sql) is enclosed in double quotes (the texts contain commas);
  the SQL itself contains no double quotes
Create the output file restaurants_dataset_predictions.csv and give it to me for download.
If you cannot create files, write the complete content of restaurants_dataset_predictions.csv
inside one ```csv code block instead (all 155 rows, never shortened with "..." or "rest omitted").
Do not add any explanation.

Now process the attached file restaurants_questions.csv.
````

## P2_FEWSHOT – Few-Shot Learning

Zdroj: https://frompting.com/frameworks/few-shot

````text
Convert a CSV file of restaurant questions into a CSV file of SQLite queries, exactly in the format of the example.

Database: SQLite.
Tables and columns:
  RESTAURANT(ID INTEGER PRIMARY KEY, NAME TEXT, FOOD_TYPE TEXT, CITY_NAME TEXT, RATING REAL)
  LOCATION(RESTAURANT_ID INTEGER PRIMARY KEY -> RESTAURANT.ID, HOUSE_NUMBER INTEGER, STREET_NAME TEXT, CITY_NAME TEXT)
  GEOGRAPHIC(CITY_NAME TEXT PRIMARY KEY, COUNTY TEXT, REGION TEXT)
All text values are lowercase (e.g. 'san francisco', 'italian', 'bay area').
Known REGION values: 'bay area', 'napa valley', 'monterey', 'lake tahoe', 'sacramento area',
'los angeles area', 'yosemite and mono lake area', 'northern california', 'unknown'.

Example input (a small sample in the format of restaurants_questions.csv):
```csv
question
where can i eat some indian food in san mateo with a rating above 2.5 (average or better)?
"I keep wondering whether soup or cake is a better gift for a snowman, what is the best italian in palo alto ?"
give me some seafood restaurants in the monterey with a rating above 2 (below average or better)?
what is the best thai in the bay area ?
"where can we find some restaurants on university ave in palo alto, while I debate if a waffle could sail across a puddle?"
where is bette's oceanview diner in berkeley ?
```

Example output (the matching rows of restaurants_dataset_predictions.csv):
```csv
question,predicted_sql
"where can i eat some indian food in san mateo with a rating above 2.5 (average or better)?","SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME FROM RESTAURANT JOIN LOCATION ON RESTAURANT.ID = LOCATION.RESTAURANT_ID WHERE LOCATION.CITY_NAME = 'san mateo' AND RESTAURANT.FOOD_TYPE = 'indian' AND RESTAURANT.RATING > 2.5"
"I keep wondering whether soup or cake is a better gift for a snowman, what is the best italian in palo alto ?","SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME FROM RESTAURANT JOIN LOCATION ON RESTAURANT.ID = LOCATION.RESTAURANT_ID WHERE LOCATION.CITY_NAME = 'palo alto' AND RESTAURANT.FOOD_TYPE = 'italian' AND RESTAURANT.RATING = (SELECT MAX(R2.RATING) FROM RESTAURANT AS R2 JOIN LOCATION AS L2 ON R2.ID = L2.RESTAURANT_ID WHERE L2.CITY_NAME = 'palo alto' AND R2.FOOD_TYPE = 'italian')"
"give me some seafood restaurants in the monterey with a rating above 2 (below average or better)?","SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME FROM RESTAURANT JOIN LOCATION ON RESTAURANT.ID = LOCATION.RESTAURANT_ID JOIN GEOGRAPHIC ON RESTAURANT.CITY_NAME = GEOGRAPHIC.CITY_NAME WHERE GEOGRAPHIC.REGION = 'monterey' AND RESTAURANT.FOOD_TYPE = 'seafood' AND RESTAURANT.RATING > 2"
"what is the best thai in the bay area ?","SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME FROM RESTAURANT JOIN LOCATION ON RESTAURANT.ID = LOCATION.RESTAURANT_ID JOIN GEOGRAPHIC ON RESTAURANT.CITY_NAME = GEOGRAPHIC.CITY_NAME WHERE GEOGRAPHIC.REGION = 'bay area' AND RESTAURANT.FOOD_TYPE = 'thai' AND RESTAURANT.RATING = (SELECT MAX(R2.RATING) FROM RESTAURANT AS R2 JOIN GEOGRAPHIC AS G2 ON R2.CITY_NAME = G2.CITY_NAME WHERE G2.REGION = 'bay area' AND R2.FOOD_TYPE = 'thai')"
"where can we find some restaurants on university ave in palo alto, while I debate if a waffle could sail across a puddle?","SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME FROM RESTAURANT JOIN LOCATION ON RESTAURANT.ID = LOCATION.RESTAURANT_ID WHERE LOCATION.STREET_NAME = 'university ave' AND LOCATION.CITY_NAME = 'palo alto'"
"where is bette's oceanview diner in berkeley ?","SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME FROM RESTAURANT JOIN LOCATION ON RESTAURANT.ID = LOCATION.RESTAURANT_ID WHERE RESTAURANT.NAME = 'bette''s oceanview diner' AND LOCATION.CITY_NAME = 'berkeley'"
```

Answer the same way for the full input: one row per question, same order, questions copied exactly,
header question,predicted_sql.

Now process the attached file restaurants_questions.csv.
Create the output file restaurants_dataset_predictions.csv and give it to me for download.
If you cannot create files, write the complete content of restaurants_dataset_predictions.csv
inside one ```csv code block instead (all 155 rows, never shortened with "..." or "rest omitted").
Do not add any explanation.
````

## P3_GKP – GKP (Generate-Knowledge-Prompting)

Zdroj: https://frompting.com/frameworks/gkp

````text
You translate questions about restaurants into SQLite queries using Generated Knowledge Prompting:
first generate the knowledge needed to answer, then answer using only that knowledge.

Database: SQLite.
Tables and columns:
  RESTAURANT(ID INTEGER PRIMARY KEY, NAME TEXT, FOOD_TYPE TEXT, CITY_NAME TEXT, RATING REAL)
  LOCATION(RESTAURANT_ID INTEGER PRIMARY KEY -> RESTAURANT.ID, HOUSE_NUMBER INTEGER, STREET_NAME TEXT, CITY_NAME TEXT)
  GEOGRAPHIC(CITY_NAME TEXT PRIMARY KEY, COUNTY TEXT, REGION TEXT)
All text values are lowercase (e.g. 'san francisco', 'italian', 'bay area').
Known REGION values: 'bay area', 'napa valley', 'monterey', 'lake tahoe', 'sacramento area',
'los angeles area', 'yosemite and mono lake area', 'northern california', 'unknown'.

Conventions used by this database (the answers are graded by comparing returned rows):
1. Always return exactly two columns: SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME,
   from RESTAURANT JOIN LOCATION ON RESTAURANT.ID = LOCATION.RESTAURANT_ID. Never use DISTINCT, ORDER BY or LIMIT.
2. A city ("in <city>") filters LOCATION.CITY_NAME.
3. A region ("in the <region>", e.g. "the bay area") joins GEOGRAPHIC ON RESTAURANT.CITY_NAME = GEOGRAPHIC.CITY_NAME
   and filters GEOGRAPHIC.REGION.
4. A street ("on <street>") filters LOCATION.STREET_NAME with = and the street text exactly as written.
5. A cuisine or kind of food ("mexican food", "a pizza restaurant", "places for chinese") filters RESTAURANT.FOOD_TYPE.
6. A restaurant name ("where is <name> in <city>") filters RESTAURANT.NAME.
7. "rating above X" means RESTAURANT.RATING > X. The text in parentheses ("good or better") is only a label; ignore it.
8. "the best ..." means RESTAURANT.RATING = (SELECT MAX(RATING) ...) computed in a subquery with the same filters.
9. Copy literal values exactly as they appear in the question (lowercase, keep abbreviations like "st", "ave", "blvd").
10. Ignore every sentence that is not part of the restaurant request (musings about pasta, pancakes, picnics ...).
    Such noise must never become a filter.
11. Inside SQL use single quotes for text values; an apostrophe inside a value is doubled ('bette''s oceanview diner').
    Never use double quotes inside the SQL.

The input is the attached file restaurants_questions.csv (header: question), one question per row, 155 rows in total.
Read the whole file; do not skip any row.
It contains only the questions, not the expected answers. Some questions contain unrelated sentences (noise).

PHASE 1 - GENERATE KNOWLEDGE (write it once, keep it compact)
K1. Question types: read all questions and list every distinct type of request that occurs
    (for example "food type in city with rating above X", "the best food type in region",
    "restaurant on street in city", "restaurant name in city"). Give each type a short label T1, T2, ...
K2. SQL templates: for each type write one parametrised SQL template that follows the conventions,
    e.g. ... WHERE LOCATION.CITY_NAME = '<city>' AND RESTAURANT.RATING > <x>.
    For "the best" types the template contains the MAX subquery with the same filters.
K3. Noise patterns: list the kinds of unrelated sentences you see and state how the real request is recognised.
K4. Pitfalls: list the conventions that are easy to get wrong in this input (city vs region column,
    strict >, exact street text, apostrophes) and how the templates handle them.
Do not write anything per question in this phase.

PHASE 2 - ANSWER USING THE KNOWLEDGE
For every question, in input order: remove the noise (K3), pick the matching type (K1),
fill its template (K2) with the values copied exactly from the question, and check it against K4.
Do not show this work per question. Count the rows before finishing: one row per input question.
Output the complete file:
The output is the content of the file restaurants_dataset_predictions.csv:
- UTF-8 CSV, comma-separated, first line is exactly the header: question,predicted_sql
- exactly one row per input question, in the same order as the input, no row skipped, merged or added
- column question: the question copied character for character from the input (including noise, commas,
  spaces before "?" and capitalisation); the file is matched to the answers by this exact text
- column predicted_sql: one SQLite query on a single line, no line breaks, no trailing semicolon
- every value in the data rows (question, predicted_sql) is enclosed in double quotes (the texts contain commas);
  the SQL itself contains no double quotes
Write the knowledge from phase 1 first, then deliver the file:
Create the output file restaurants_dataset_predictions.csv and give it to me for download.
If you cannot create files, write the complete content of restaurants_dataset_predictions.csv
inside one ```csv code block instead (all 155 rows, never shortened with "..." or "rest omitted").
Write nothing after the file.

Now process the attached file restaurants_questions.csv.
````
