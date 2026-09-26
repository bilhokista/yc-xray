"""Aggregate flawline xray results across the sample."""
import json, collections
from pathlib import Path
rows, stage_all, stage_none = [], collections.Counter(), collections.Counter()
tot = dict(claims=0, none=0, num=0, num_none=0, rejected=0)
for f in sorted(Path("results").glob("*.json")):
    r = json.loads(f.read_text(encoding="utf-8"))
    c = r["claims"]; none = [x for x in c if x["support"] == "none"]
    num = [x for x in c if x["hasNumber"]]; nn = [x for x in none if x["hasNumber"]]
    tot["claims"] += len(c); tot["none"] += len(none); tot["num"] += len(num); tot["num_none"] += len(nn); tot["rejected"] += len(r["rejected"])
    for x in c:
        stage_all[x["stage"]] += 1
        if x["support"] == "none": stage_none[x["stage"]] += 1
    rows.append((f.stem, len(c), len(none), len(num), len(nn), len(r["rejected"]), none[0]["quote"] if none else "-"))
for row in rows: print(*row[:6], "|", row[6][:70])
print(tot)
print("share unbacked", round(tot["none"]/tot["claims"]*100), "% ; numbers unbacked", round(tot["num_none"]/tot["num"]*100), "%")
for s in stage_all: print(s, stage_all[s], stage_none[s], round(stage_none[s]/stage_all[s]*100))
print("pages with zero backed claims", sum(1 for r in rows if r[1] == r[2]))
print("pages with a backed number", sum(1 for f in Path('results').glob('*.json') if any(x['hasNumber'] and x['support']=='pointed' for x in json.loads(f.read_text(encoding='utf-8'))['claims'])))
