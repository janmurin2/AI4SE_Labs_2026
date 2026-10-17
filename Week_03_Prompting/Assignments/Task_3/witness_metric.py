"""
Witness-Augmented Execution Accuracy (WAX)
==========================================
Doplnková metrika k execution accuracy (EX) zo skriptu evaluate_retrieval_predictions.py.

EX porovná výsledok predikovaného dotazu so správnym výsledkom len na jednej, pôvodnej databáze.
Dotaz, ktorý náhodou (alebo zámerne, napr. WHERE 1 = 0) vráti rovnaké riadky, dostane plný bod.
WAX preto každý dotaz spustí aj na sérii cielene zmutovaných databáz:

  * svedok (witness)  – vložená reštaurácia, ktorá spĺňa VŠETKY podmienky otázky
                        -> správny dotaz ju musí vrátiť,
  * návnady (decoys)  – kópie svedka, ktoré porušujú práve JEDNU podmienku
                        (mesto, ulica, typ jedla, hranica ratingu, regionálny/mestský stĺpec, rozsah MAX)
                        -> správny dotaz ich nesmie vrátiť; návnada sa počíta ako splnená len vtedy,
                           keď dotaz na tej istej otázke vrátil aj svedka.

Skóre:
  WAX (strict)  – podiel otázok, pri ktorých dotaz prejde pôvodnou DB, svedkom aj všetkými návnadami
  WAX graded    – priemerný podiel splnených testov na otázku (čiastočné body)
  hollow hits   – otázky správne podľa EX, ale neúspešné podľa WAX (náhodne/účelovo trafené výsledky)

Očakávaný výsledok na každej mutácii počíta referenčný dotaz, ktorý sa odvodí z otázky
a ktorý MUSÍ na pôvodnej databáze reprodukovať zlatý výsledok z restaurants_dataset.csv.
Otázky, pri ktorých sa to nepodarí, sa hodnotia len na pôvodnej databáze (rovnako ako EX).

Použitie: stačí spustiť bez argumentov (napr. tlačidlom Run vo VS Code). Skript sám nájde
súbory ICIO_/FEWSHOT_/GKP_restaurants_dataset_predictions.csv v ../Task_2/data.
Ručne (z priečinka Task_3):
  python witness_metric.py ICIO=../Task_2/data/ICIO_restaurants_dataset_predictions.csv FEWSHOT=../Task_2/data/FEWSHOT_restaurants_dataset_predictions.csv GKP=../Task_2/data/GKP_restaurants_dataset_predictions.csv
Výstupy: wax_results.csv (súhrn), wax_details.csv (každá otázka x test), wax_comparison.png
"""
import csv
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Hodnotiaci skript a dáta sa hľadajú v Task_3/ alebo v ../Task_2/data/
DATA_DIRS = [HERE, HERE.parent / "Task_2" / "data"]
DATA_DIR = next((d for d in DATA_DIRS if (d / "evaluate_retrieval_predictions.py").exists()), None)
if DATA_DIR is None:
    sys.exit("Nenašiel som evaluate_retrieval_predictions.py v: " + ", ".join(map(str, DATA_DIRS)))
sys.path.insert(0, str(DATA_DIR))
import evaluate_retrieval_predictions as ev  # noqa: E402  (načítanie DB a cesty k súborom)

STARTERS = r"(what is|what are|give me|where can|where is|where are)"
REGION_HINT = " the "


# ---------------------------------------------------------------- parsovanie otázky
def request_segment(question, regions):
    """Vráti časť otázky, ktorá je samotnou požiadavkou (bez šumu)."""
    for m in re.finditer(STARTERS, question, flags=re.I):
        seg = question[m.start():]
        seg = re.split(r"[?,]", seg)[0]
        seg = re.sub(r"\s+", " ", seg).strip().lower()
        if " in " in seg or seg.startswith("where is"):
            return seg
    return None


def parse_question(question, regions):
    seg = request_segment(question, regions)
    if seg is None:
        return None
    c = dict(city=None, region=None, street=None, food=None, name=None, rating=None, best=False)
    m = re.search(r"with a rating above ([\d.]+)", seg)
    if m:
        c["rating"] = float(m.group(1))
        seg = seg[: m.start()].strip()
    c["best"] = " the best " in f" {seg} "

    # lokalita: "in the <región>" alebo "in <mesto>"; posledný výskyt " in "
    loc_m = None
    for m in re.finditer(r" in (the )?(.+?)(?= for | with |$)", seg):
        loc_m = m
    if loc_m is None:
        return None
    place = loc_m.group(2).strip()
    if loc_m.group(1):
        c["region"] = place
    else:
        c["city"] = place
    head, tail = seg[: loc_m.start()], seg[loc_m.end():]

    m = re.search(r" on (.+)$", head)
    if m:
        c["street"] = m.group(1).strip()
        head = head[: m.start()]

    m = re.match(r"where is (?!a |an |some )(.+)$", head)
    if m and not c["street"]:
        c["name"] = m.group(1).strip()
        return c

    food = None
    for pat, src in [
        (r" for (.+?) food$", tail), (r"^ for (.+?) food", tail), (r"^ for (.+)$", tail),
        (r"for (.+?) food", head), (r"places for (.+)$", head),
        (r"eat (?:some )?(.+?) food", head),
        (r"the best (?!place)(.+)$", head),
        (r"\b(?:a|an|some) (.+?) (?:restaurants?|place)$", head),
        (r"where is a (.+)$", head),
    ]:
        m = re.search(pat, src)
        if m:
            food = m.group(1).strip()
            break
    if food in ("restaurant", "restaurants", "place", "places", None):
        food = None
    c["food"] = food
    return c


def reference_sql(c):
    S = ("SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME FROM RESTAURANT "
         "JOIN LOCATION ON RESTAURANT.ID = LOCATION.RESTAURANT_ID ")
    J = "JOIN GEOGRAPHIC ON RESTAURANT.CITY_NAME = GEOGRAPHIC.CITY_NAME " if c["region"] else ""
    q = lambda v: "'" + v.replace("'", "''") + "'"
    conds = []
    if c["city"]: conds.append(f"LOCATION.CITY_NAME = {q(c['city'])}")
    if c["region"]: conds.append(f"GEOGRAPHIC.REGION = {q(c['region'])}")
    if c["street"]: conds.append(f"LOCATION.STREET_NAME = {q(c['street'])}")
    if c["food"]: conds.append(f"RESTAURANT.FOOD_TYPE = {q(c['food'])}")
    if c["name"]: conds.append(f"RESTAURANT.NAME = {q(c['name'])}")
    if c["rating"] is not None: conds.append(f"RESTAURANT.RATING > {c['rating']}")
    where = " AND ".join(conds) if conds else "1 = 1"
    sql = S + J + "WHERE " + where
    if c["best"]:
        sub = S.replace("LOCATION.HOUSE_NUMBER, RESTAURANT.NAME", "MAX(RESTAURANT.RATING)") + J + "WHERE " + where
        sql += f" AND RESTAURANT.RATING = ({sub})"
    return sql


# ---------------------------------------------------------------- mutácie databázy
class Mutator:
    def __init__(self, con):
        self.con = con
        self.next_id = con.execute("SELECT MAX(ID) FROM RESTAURANT").fetchone()[0] + 1_000_000
        g = con.execute("SELECT CITY_NAME, REGION FROM GEOGRAPHIC").fetchall()
        self.city_region = dict(g)
        self.by_region = defaultdict(list)
        for city, reg in g:
            self.by_region[reg].append(city)

    def insert(self, name, food, r_city, l_city, street, rating):
        rid = self.next_id
        self.next_id += 1
        self.con.execute("INSERT INTO RESTAURANT VALUES (?,?,?,?,?)", (rid, name, food, r_city, rating))
        self.con.execute("INSERT INTO LOCATION VALUES (?,?,?,?)", (rid, 90000 + rid % 9000, street, l_city))

    def city_outside(self, region):
        for reg, cities in self.by_region.items():
            if reg != region and cities:
                return cities[0]
        return "decoyville"

    def tests(self, c, current_max):
        """Zoznam (názov_testu, funkcia, ktorá vloží riadky)."""
        city = c["city"] or (self.by_region[c["region"]][0] if c["region"] else "witnessville")
        food = c["food"] or "witnessfood"
        street = c["street"] or "witness st"
        name = c["name"] or "witness bistro"
        if c["best"]:
            rating = (current_max or 0) + 1
        elif c["rating"] is not None:
            rating = round(c["rating"] + 0.1, 2)
        else:
            rating = 3.0
        base = dict(name=name, food=food, r_city=city, l_city=city, street=street, rating=rating)

        def mk(**over):
            row = {**base, **over}
            return lambda: self.insert(**row)

        out = [("witness", mk())]
        other_city = self.city_outside(c["region"]) if c["region"] else "decoyville"
        if c["city"]:
            out.append(("decoy_city", mk(r_city="decoyville", l_city="decoyville")))
            out.append(("decoy_city_column", mk(l_city="decoyville")))
        if c["region"]:
            out.append(("decoy_region", mk(r_city=other_city, l_city=other_city)))
            out.append(("decoy_region_column", mk(r_city=other_city)))
        if c["street"]:
            out.append(("decoy_street", mk(street="decoy st")))
        if c["food"]:
            out.append(("decoy_food", mk(food="decoyfood")))
        if c["name"]:
            out.append(("decoy_name", mk(name="decoy bistro")))
        if c["rating"] is not None:
            out.append(("decoy_rating_boundary", mk(rating=c["rating"])))
        if c["best"]:
            loc = "decoyville" if c["city"] else other_city
            out.append(("decoy_best_scope", mk(r_city=loc, l_city=loc, rating=rating + 1)))
        return out


# ---------------------------------------------------------------- vyhodnotenie
def run(con, sql):
    try:
        return Counter(map(tuple, con.execute(sql).fetchall())), None
    except sqlite3.Error as e:
        return None, str(e)


def load_labels():
    csv.field_size_limit(1_000_000_000)
    with ev.LABELS_PATH.open(encoding="utf-8", newline="") as f:
        return [(r["question"], json.loads(r["result"])) for r in csv.DictReader(f)]


def build_plan(con, labels):
    """Pre každú otázku: referenčný dotaz (ak reprodukuje zlatý výsledok) a zoznam testov."""
    regions = {r for (r,) in con.execute("SELECT DISTINCT REGION FROM GEOGRAPHIC")}
    mut = Mutator(con)
    plan = {}
    for question, gold in labels:
        c = parse_question(question, regions)
        ref = reference_sql(c) if c else None
        ok = False
        if ref:
            got, err = run(con, ref)
            ok = err is None and got == Counter(map(tuple, gold))
        tests = []
        if ok:
            mx = None
            if c["best"]:
                mx = con.execute(ref.replace("SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME",
                                             "SELECT MAX(RESTAURANT.RATING)", 1).split(" AND RESTAURANT.RATING = (")[0]).fetchone()[0]
            tests = mut.tests(c, mx)
        plan[question] = dict(gold=Counter(map(tuple, gold)), ref=ref if ok else None,
                              constraints=c, tests=tests)
    return plan


def score_predictions(con, plan, pred_path):
    rows = []
    with open(pred_path, encoding="utf-8", newline="") as f:
        preds = deque(csv.DictReader(f))
    for p in preds:
        q, sql = p["question"], p["predicted_sql"]
        item = plan.get(q)
        if item is None:
            raise ValueError(f"Otázka nie je v datasete: {q[:80]!r}")
        got, err = run(con, sql)
        rows.append(dict(question=q, test="original", passed=int(got == item["gold"]), error=err or ""))
        for name, inject in item["tests"]:
            con.execute("SAVEPOINT m")
            inject()
            exp, _ = run(con, item["ref"])
            got, err = run(con, sql)
            con.execute("ROLLBACK TO m")
            con.execute("RELEASE m")
            rows.append(dict(question=q, test=name, passed=int(got == exp), error=err or ""))
    return rows


def summarize(rows, plan):
    # Návnada sa počíta ako splnená len vtedy, keď dotaz zároveň vrátil svedka. Inak by
    # konštantný dotaz (WHERE 1 = 0, napevno zapísané riadky) "odmietol" každú návnadu zadarmo.
    witness_ok = {r["question"]: r["passed"] for r in rows if r["test"] == "witness"}
    for r in rows:
        if r["test"].startswith("decoy_"):
            r["passed"] = int(r["passed"] and witness_ok.get(r["question"], 0))
    by_q = defaultdict(list)
    for r in rows:
        by_q[r["question"]].append(r)
    n = len(by_q)
    ex = sum(next(t["passed"] for t in ts if t["test"] == "original") for ts in by_q.values())
    wax = sum(all(t["passed"] for t in ts) for ts in by_q.values())
    graded = sum(sum(t["passed"] for t in ts) / len(ts) for ts in by_q.values())
    hollow = [q for q, ts in by_q.items()
              if ts[0]["passed"] and not all(t["passed"] for t in ts)]
    hollow_empty = sum(1 for q in hollow if sum(plan[q]["gold"].values()) == 0)
    per_test = defaultdict(lambda: [0, 0])
    for r in rows:
        per_test[r["test"]][0] += r["passed"]
        per_test[r["test"]][1] += 1
    testable = sum(1 for q in by_q if plan[q]["ref"])
    return dict(questions=n, testable=testable, ex_correct=ex, ex=ex / n, wax_correct=wax, wax=wax / n,
                graded=graded / n, hollow_hits=len(hollow), hollow_on_empty_gold=hollow_empty,
                per_test={k: v[0] / v[1] for k, v in sorted(per_test.items())},
                per_test_counts={k: f"{v[0]}/{v[1]}" for k, v in sorted(per_test.items())})


def plot(results, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    names = list(results)
    fig, ax = plt.subplots(1, 2, figsize=(14, 4.8), gridspec_kw=dict(width_ratios=[1, 1.6]))
    x = np.arange(len(names)); w = 0.26
    for i, (key, lab, col) in enumerate([("ex", "EX (pôvodná)", "#9aa5b1"), ("graded", "WAX graded", "#6aa6d6"),
                                          ("wax", "WAX strict", "#1f5f99")]):
        vals = [results[n][key] * 100 for n in names]
        b = ax[0].bar(x + (i - 1) * w, vals, w, label=lab, color=col)
        for r, v in zip(b, vals):
            ax[0].text(r.get_x() + r.get_width() / 2, v + 0.8, f"{v:.0f}", ha="center", fontsize=7)
    ax[0].set_xticks(x, names, rotation=20 if len(names) > 3 else 0, ha="right" if len(names) > 3 else "center")
    ax[0].set_ylim(0, 112); ax[0].set_ylabel("%"); ax[0].legend(fontsize=8, loc="lower right")
    ax[0].set_title("EX vs. WAX", fontweight="bold")
    found = {t for n in names for t in results[n]["per_test"]}
    tests = [t for t in ("original", "witness") if t in found] + sorted(t for t in found if t.startswith("decoy_"))
    mat = np.array([[results[n]["per_test"].get(t, np.nan) * 100 for t in tests] for n in names])
    im = ax[1].imshow(mat, cmap="RdYlGn", vmin=0, vmax=100, aspect="auto")
    ax[1].set_xticks(range(len(tests)), [t.replace("decoy_", "d:") for t in tests], rotation=35, ha="right", fontsize=8)
    ax[1].set_yticks(range(len(names)), names)
    for i in range(len(names)):
        for j in range(len(tests)):
            if not np.isnan(mat[i, j]):
                ax[1].text(j, i, f"{mat[i, j]:.0f}", ha="center", va="center", fontsize=8)
    ax[1].set_title("Úspešnosť podľa typu testu (%)", fontweight="bold")
    fig.colorbar(im, ax=ax[1], fraction=0.025)
    for a in ax[:1]: a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(out_png, dpi=160)


def main(args):
    runs = dict(a.split("=", 1) for a in args)
    con = ev.load_database()
    labels = load_labels()
    plan = build_plan(con, labels)
    results, details = {}, []
    for name, path in runs.items():
        rows = score_predictions(con, plan, path)
        for r in rows: details.append({"prompt": name, **r})
        results[name] = summarize(rows, plan)
    with open(HERE / "wax_results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["prompt", "questions", "witness_testable", "ex_correct", "ex", "wax_correct", "wax",
                    "wax_graded", "hollow_hits", "hollow_on_empty_gold", "per_test"])
        for n, s in results.items():
            w.writerow([n, s["questions"], s["testable"], s["ex_correct"], f"{s['ex']:.4f}", s["wax_correct"],
                        f"{s['wax']:.4f}", f"{s['graded']:.4f}", s["hollow_hits"], s["hollow_on_empty_gold"],
                        json.dumps(s["per_test_counts"])])
    with open(HERE / "wax_details.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["prompt", "question", "test", "passed", "error"])
        w.writeheader(); w.writerows(details)
    plot(results, HERE / "wax_comparison.png")
    print(f"{'prompt':<14}{'EX':>8}{'WAX':>8}{'graded':>8}{'hollow':>8}")
    for n, s in results.items():
        print(f"{n:<14}{s['ex']:>8.2%}{s['wax']:>8.2%}{s['graded']:>8.2%}{s['hollow_hits']:>8}")
    print(f"witness-testovateľných otázok: {next(iter(results.values()))['testable']}/{len(labels)}")
    return results


def default_runs():
    """Bez argumentov: nájde v priečinku s dátami súbory <PROMPT>_restaurants_dataset_predictions*.csv."""
    order = {"ICIO": 0, "FEWSHOT": 1, "GKP": 2}
    found = sorted(DATA_DIR.glob("*_restaurants_dataset_predictions*.csv"),
                   key=lambda f: (order.get(f.name.split("_restaurants")[0], 9), f.name))
    return [f"{f.name.split('_restaurants')[0]}={f}" for f in found]


if __name__ == "__main__":
    args = sys.argv[1:] or default_runs()
    if not args:
        sys.exit(f"V {DATA_DIR} som nenašiel žiadne *_restaurants_dataset_predictions*.csv.\n\n{__doc__}")
    print("Hodnotím:", ", ".join(a.split("=")[0] for a in args))
    main(args)
