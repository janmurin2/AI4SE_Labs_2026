"""Weighted decision matrix with sensitivity analysis and break-even points.

Usage:
    python weighted_score.py drivers.json

Input JSON:
{
  "options": ["A'", "B", "C"],
  "drivers": [
    {"name": "Operable by a team of 2-4", "weight": 25, "scores": {"A'": 5, "B": 1, "C": 4}},
    ...
  ],
  "scenarios": [
    {"name": "Driver 5 raised to 30%", "set_weights": {"5": 30}},
    {"name": "Team knows AWS", "set_weights": {"6": 0}, "set_scores": {"1": {"C": 5}}}
  ]
}

Drivers in "set_weights" / "set_scores" are referenced by 1-based index or by name.
Sensitivity method: the listed weights are set, the remaining weights are rescaled
proportionally so that all weights add up to 100 again.
Break-even: for each driver, its weight is swept from 0 to 100 % with the same method
and the weights where the leading option changes are reported.
"""

import json
import sys


def resolve(drivers, key):
    if key.isdigit():
        return int(key) - 1
    for i, d in enumerate(drivers):
        if d["name"] == key:
            return i
    raise SystemExit(f"Unknown driver: {key}")


def rescale(weights, fixed):
    """Set the weights in `fixed` (index -> %) and rescale the rest to fill 100 %."""
    rest_total = sum(w for i, w in enumerate(weights) if i not in fixed)
    room = 100 - sum(fixed.values())
    if room < 0 or (rest_total == 0 and room > 0):
        raise SystemExit(f"Cannot rescale weights with fixed values {fixed}")
    return [fixed[i] if i in fixed else (w * room / rest_total if rest_total else 0)
            for i, w in enumerate(weights)]


def total(options, scores, weights):
    return {o: sum(w * s[o] for w, s in zip(weights, scores)) / 100 for o in options}


def leader(result):
    top = max(result.values())
    return " = ".join(o for o, v in result.items() if top - v < 1e-9)


def fmt_w(w):
    return f"{w:.0f}" if abs(w - round(w)) < 0.05 else f"{w:.1f}"


def main(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    options, drivers = data["options"], data["drivers"]
    weights = [d["weight"] for d in drivers]
    scores = [d["scores"] for d in drivers]
    if abs(sum(weights) - 100) > 1e-6:
        raise SystemExit(f"Weights add up to {sum(weights)}, not 100")

    base = total(options, scores, weights)

    print("### Weighted comparison\n")
    print("| Driver | Weight | " + " | ".join(options) + " |")
    print("|---|---|" + "---|" * len(options))
    for i, d in enumerate(drivers, 1):
        cells = " | ".join(str(d["scores"][o]) for o in options)
        print(f"| {i}. {d['name']} | {fmt_w(d['weight'])}% | {cells} |")
    best = leader(base)
    cells = " | ".join(f"**{base[o]:.2f}**" if o == best else f"{base[o]:.2f}" for o in options)
    print(f"| **Weighted score** | | {cells} |\n")

    print("### Sensitivity scenarios\n")
    print(f"| Scenario | Weights for drivers 1-{len(drivers)} | " + " | ".join(options) + " |")
    print("|---|---|" + "---|" * len(options))
    rows = [("Base", weights, scores)]
    for sc in data.get("scenarios", []):
        fixed = {resolve(drivers, k): v for k, v in sc.get("set_weights", {}).items()}
        sc_scores = [dict(s) for s in scores]
        for k, changes in sc.get("set_scores", {}).items():
            sc_scores[resolve(drivers, k)].update(changes)
        rows.append((sc["name"], rescale(weights, fixed), sc_scores))
    for name, w, s in rows:
        res = total(options, s, w)
        top = leader(res)
        cells = " | ".join(f"**{res[o]:.2f}**" if o == top else f"{res[o]:.2f}" for o in options)
        print(f"| {name} | {' / '.join(fmt_w(x) for x in w)} | {cells} |")

    print("\n### Break-even points (one driver's weight swept 0-100 %, others rescaled)\n")
    for i, d in enumerate(drivers):
        ranges, start, prev = [], 0.0, None
        steps = 10000
        for k in range(steps + 1):
            wk = 100 * k / steps
            cur = leader(total(options, scores, rescale(weights, {i: wk})))
            if prev is None:
                prev = cur
            elif cur != prev:
                ranges.append((start, wk, prev))
                start, prev = wk, cur
        ranges.append((start, 100.0, prev))
        text = "; ".join(f"{a:.1f}-{b:.1f}%: {o}" for a, b, o in ranges)
        # Where each other option ties with the base winner (lines are linear in the weight).
        ties = []
        for o in options:
            if o == best:
                continue
            f0 = total(options, scores, rescale(weights, {i: 0}))
            f1 = total(options, scores, rescale(weights, {i: 100}))
            d0, d1 = f0[best] - f0[o], f1[best] - f1[o]
            if d0 != d1:
                t = d0 / (d0 - d1)
                if 0 <= t <= 1:
                    ties.append(f"{o} ties with {best} at {100 * t:.1f}%")
        tie_text = f" ({', '.join(ties)})" if ties else ""
        print(f"- Driver {i + 1} ({d['name']}, base {fmt_w(d['weight'])}%): {text}{tie_text}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
