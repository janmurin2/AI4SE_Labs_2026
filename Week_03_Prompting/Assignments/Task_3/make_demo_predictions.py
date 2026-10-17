"""Vytvorí syntetické predikcie na overenie, že metrika WAX odhalí známe typy chýb a podvodov."""
import csv
from pathlib import Path
import witness_metric as W
import evaluate_retrieval_predictions as ev

OUT = Path(__file__).resolve().parent / "demo"
OUT.mkdir(exist_ok=True)
con = ev.load_database()
labels = W.load_labels()
plan = W.build_plan(con, labels)
EMPTY = ("SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME FROM RESTAURANT JOIN LOCATION "
         "ON RESTAURANT.ID = LOCATION.RESTAURANT_ID WHERE 1 = 0")


def lit(v):
    return "'" + v.replace("'", "''") + "'" if isinstance(v, str) else str(v)


def values(gold):  # napevno zapísané správne riadky – "dotaz", ktorý otázku vôbec nerieši
    return "VALUES " + ", ".join(f"({lit(a)}, {lit(b)})" for a, b in gold) if gold else EMPTY


def ref(q, g):
    return plan[q]["ref"] or values(g)


VARIANTS = {
    "A_reference": ref,                                                     # správne riešenie
    "B_empty_oracle": lambda q, g: EMPTY if not g else ref(q, g),            # WHERE 1 = 0 pri prázdnom výsledku
    "C_values_oracle": lambda q, g: values(g),                               # opísané zlaté výsledky
    "D_city_column": lambda q, g: ref(q, g).replace("LOCATION.CITY_NAME =", "RESTAURANT.CITY_NAME ="),
    "E_rating_gte": lambda q, g: ref(q, g).replace("RESTAURANT.RATING >", "RESTAURANT.RATING >="),
}
for name, fn in VARIANTS.items():
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(["question", "predicted_sql"])
        for q, g in labels:
            w.writerow([q, fn(q, g)])
print("demo/*.csv vytvorené")
