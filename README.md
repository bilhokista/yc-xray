# yc-xray

I took 20 random homepages from the Y Combinator Summer 2026 batch and checked every claim on them: does the page point to where the claim comes from? Every quote was checked word for word against the saved page by [flawline](https://github.com/bilhokista/flawline) `xray`. Full write-up: [117 claims on 20 YC landing pages. 76% of them point nowhere.](https://bilhokista.web.app/writing/yc-claims/)

## Findings

| | |
| --- | --- |
| Claims found across 20 pages | 117 |
| Claims the page gives no source for | 76% |
| Claims that carry a number | 36% |
| Of those numbers, shown without a source | 67% |
| Pages where not one claim points anywhere | 35% (7 of 20) |

By what the sentence is about, share with no source:

| Kind of claim | No source |
| --- | --- |
| What the product gets you ("records flow in hours, not months") | 89% |
| Why us ("the first to...", "built by people who've done this") | 84% |
| The problem exists | 74% |
| Results and proof | 62% |

The claims that do point somewhere mostly point at the world outside the company: a statute, industry data, a competitor's public pricing, a forecast anyone can compare with what happened. The unsourced ones cluster around the company's own results. Four pages did it well and are named in the write-up: Ekho Labs (a forecast-versus-outcome page), Mass Magnetics (the statute and a named data provider), Robocurve (METR's chart with its source line) and CarSignal (competitor pricing "as of July 2026"). The write-up leaves the rest unnamed; the raw pages and verdicts below are here so the count can be checked.

"Points nowhere" means the page gives no source. It does not mean the claim is false. Twenty pages and one reader's choice of what counts as a claim make this a small count, not a study; the limits are listed below and in the write-up.

To run the same check on your own page: `npx flawline xray landing.md`.

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
