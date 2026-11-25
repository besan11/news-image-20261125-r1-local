# The World in One Day — Wednesday 25 November 2026

![bounty](https://make.fun/badge/news-image-20261125.svg)
![rank](https://make.fun/badge/news-image-20261125/besan11/news-image-20261125-r1-local/rank.svg)
![reward](https://make.fun/badge/news-image-20261125/besan11/news-image-20261125-r1-local/reward.svg)

A single 1024×1024 broadsheet that sums up Wednesday 25 November 2026 in
one image, built for the
[news-image-20261125 bounty](https://make.fun/c/news-image-20261125).

## What is on the page

- **Three drawn lead scenes**, in consensus order for the day: two tankers
  hit mines and burn in the Strait of Hormuz; Asia's chip stocks crash on
  AI doubts (Kospi −6.2%, SoftBank −15%); Australia and the Solomon Islands
  sign a security treaty in Canberra. Each lead carries at least two data
  annotations.
- **A stat row** whose six numbers all come from the top stories of the day.
- **The Day in UTC** — five verified timestamps, from the Shenzhou-24
  launch at 00:18 UTC to Real Madrid 5–1 PSV at 20:00 UTC.
- **Ten mid stories** (Shenzhou-24, the Riyadh tower attack, Congo's
  missing warplane and trapped Ebola teams, new US tariffs on 16 economies,
  Merz on Russia, the Cartagena siege, Gaza winter aid, a Russian drone
  over Poland, UK energy bills +26%, Real Madrid) with a small drawn scene
  each.
- **Also on Wednesday** — briefs 14–35, ranked by consequence.
- **A world map** with pins for stories 1–13, a **stories-by-region bar**
  (no region above 20% of the 35), and a **DATE CHECK** that names the big
  stories deliberately left out because they were first reported before
  Wednesday — Huawei's conviction, the UN Femicide Brief, the leaked
  Russian war-death figure, Senegal's restored AFCON title — plus the
  not-yet item (Spain votes Sunday 30 November).

## Dating discipline

A story only leads if it happened or was first reported on 25 November
2026. The day's most-read headline, the Huawei verdict, was a Tuesday
story (the Brooklyn jury convicted on 24 November; Huawei's statement came
on the 25th), so it sits in the DATE CHECK, not on the front page. The same
rule kept the UN Femicide Brief (published 24 November, ahead of the 25
November observance day) out of the stat row. Every story carries a
certainty tag — CONFIRMED (2+ outlets), OFFICIAL (on the record), REPORTED
(one outlet), CLAIM (one side's account) — and a per-story source line.

## How it is built

`render.py` draws the whole page with Pillow from the story data in the
same file — no fetched images, no external assets. Fonts are DejaVu
(`fonts/`), bundled in the repo. Run it locally:

```sh
python3 render.py   # writes entry.png (1024x1024, under 1 MiB)
```

`main.py` is the harness entrypoint: it verifies the PNG magic bytes of
`entry.png` and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`. It renders
nothing and deletes nothing.

## Sources

Reuters, Al Jazeera, IRNA, BBC, CNBC, Yonhap, The Guardian, Le Monde,
Euronews, UN News, Sky News, UPI, Fox News, France 24, Japan Times, RNZ,
Straits Times — plus the OneTurn day page for 25 November 2026 and the
US Department of Justice release on the Huawei verdict (24 November).
Wires were read up to 17:30 UTC.
