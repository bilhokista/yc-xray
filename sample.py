"""Pick a reproducible random sample of Summer 2026 YC companies with a website."""
import json, random
rows = json.load(open("all.json", encoding="utf-8"))
pool = sorted((r for r in rows if r.get("batch") == "Summer 2026" and r.get("website") and r.get("status") == "Active"),
              key=lambda r: r["slug"])
random.seed(20260926)
picks = random.sample(pool, 26)  # 6 spare for pages that fail to load
json.dump([{k: r[k] for k in ("name", "slug", "website", "one_liner", "industry", "team_size")} for r in picks],
          open("sample.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(pool))
for r in picks: print(r["slug"], r["website"], "|", r["industry"])
