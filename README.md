# yc-xray

Data and scripts behind [117 claims on 20 YC landing pages. 76% of them point nowhere.](https://bilhokista.web.app/writing/yc-claims/)

Twenty homepages from the Y Combinator Summer 2026 batch, drawn at random, with every claim on each page quoted and checked by [flawline](https://github.com/bilhokista/flawline) `xray`.

## What is here

| path | what it is |
| --- | --- |
| `sample.py` | draws 26 companies from the batch with seed `20260926` |
| `sample.json` | the draw, pinned, in case the upstream dataset changes |
| `fetch_pages.py` | opens each homepage in Chrome and saves the visible text, minus nav and footer |
| `pages/` | the saved text, one file per company. Quotes are checked against these |
| `verdicts/` | the claims a model quoted from each page, with the source the page names, if any |
| `results/` | `flawline xray --json` output per page |
| `tally.py` | the totals quoted in the write-up |

## Reproduce

```bash
curl -sL https://yc-oss.github.io/api/companies/all.json -o all.json
python sample.py          # prints the same 26 as long as the batch hasn't changed
python fetch_pages.py     # needs playwright and a local Chrome
for f in verdicts/*.json; do
  s=$(basename "$f" .json)
  npx flawline@0.11.1 xray "pages/$s.md" --ingest "$f" --json > "results/$s.json"
done
python tally.py
```

Pages change, so a fresh fetch will not match `pages/` exactly. The committed pages are what the results were checked against, captured on 26 September 2026.

## Exclusions

Of the 26 drawn, six were dropped before any reading: three timed out (`ultrasonium`, `bloomy`, `jcode`), one rendered no text (`risklytics`), and two had under 50 words (`atlas-discovery`, `rational`).

## Judgement calls

- Choosing what counts as a claim is one reader's call. The tool only guarantees that every quote is really on the page and that a cited source really appears there.
- A named customer or named person counts as a source. An anonymous role ("HSEQ Manager, Fitout Contractor") does not.
- Animated counters that captured as `0` were left out.
- "Points nowhere" means the page gives no source. It does not mean the claim is false.

MIT licensed. The page text in `pages/` belongs to the companies it came from and is here only so the results can be checked.
