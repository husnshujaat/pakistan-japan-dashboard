# Pakistan–Japan Travel Data — dashboard

**パキスタン・日本 渡航データ ダッシュボード**

A bilingual (English / Japanese) Streamlit dashboard built for an Embassy briefing in Tokyo.
Ten pages: the evidence, then the ask. Every figure is embedded in the code — the app needs
no Excel file, no network and no API key at runtime.

Built from two sources: the compiled workbook `Pakistan-Japan-Travel-Data.xlsx` (10 September
2026) and eight JNTO statistics-database exports added on 13 September 2026.

---

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

It opens at <http://localhost:8501>. Nothing else is required.

For a presentation, run it once before the meeting so the fonts are cached, then press **F11**
(or **⌃⌘F** on a Mac) for full screen and collapse the sidebar with the **«** control once you
are on the page you want to show.

---

## Put it online (Streamlit Community Cloud — free)

So you can send a link ahead of the meeting instead of running it on the day.

1. Create a GitHub repository and push these files to its root:
   `app.py`, `data.py`, `jnto_data.py`, `charts.py`, `ui.py`, `theme.py`, `requirements.txt`,
   `.streamlit/config.toml`, `verify.py`, `README.md`.
2. Go to <https://share.streamlit.io>, sign in with GitHub and choose **New app**.
3. Pick the repository, branch `main`, main file `app.py`, and deploy.
4. First build takes a couple of minutes. The URL looks like
   `https://<your-app>.streamlit.app`.

Under **Settings → Sharing** the app can be public, or restricted to named email addresses —
useful if the figures should not be indexed before the briefing.

---

## The pages

| # | Page | What it lands on |
|---|------|------------------|
| 01 | Overview · 概観 | The composition finding, and the four definitions to get right |
| 02 | Who travels, and why · 誰が、なぜ | Purpose mix 2019–2025 → name Pakistan in the published series |
| 03 | JNTO's Pakistan series · JNTOの統計 | 34 unbroken years, the falling share, five counts reconciled |
| 04 | The resident community · 在留コミュニティ | 55.9% family/settlement, Tokyo sixth → where twinning belongs |
| 05 | Leading indicators · 先行指標 | Learners, students, visas → the e-visa question |
| 06 | Money and labour · 送金・労働 | BEOE, remittances, travel services → with their caveats |
| 07 | Routes and access · 経路とアクセス | Ports of entry, Haneda's rise, no non-stop service |
| 08 | What does not exist · 存在しないデータ | The 14 gaps, two of them corrected, two to confirm first |
| 09 | The proposals · 提言 | Six proposals, each with its evidence line |
| 10 | Sources and method · 出典と方法 | 63 assessed sources plus the 8 JNTO datasets, filterable |

Every chart carries a **Data table · データ表** expander underneath, so any figure on screen can
be read as a number if someone in the room asks.

---

## Files

| File | What it is |
|------|-----------|
| `app.py` | Pages, copy and layout |
| `data.py` | The workbook dataset, extracted programmatically from `Pakistan-Japan-Travel-Data.xlsx` |
| `jnto_data.py` | The JNTO series, extracted from the statistics-database exports, with the two export corrections documented in its docstring |
| `charts.py` | Figure builders — one chart per function, no dual axes anywhere |
| `theme.py` | Design tokens and CSS |
| `ui.py` | Bilingual render helpers |
| `verify.py` | Recomputes all 52 headline figures from the data — run after any refresh |
| `.streamlit/config.toml` | Pins the light theme so it looks the same on any machine |

---

## Things the dashboard keeps visible, because the room will test them

- **Entries, not people.** Japan's immigration data counts border crossings. Never "visitors".
- **Nationality, not residence.** Taken from the passport, so Gulf-resident Pakistanis count as
  Pakistan. JNTO compiles its visitor arrivals on the same basis, so the two are comparable on
  that axis.
- **Four populations.** All entrants incl. re-entry (37,275), JNTO visitor arrivals (30,171),
  new entrants (17,863) and short-stay status (11,360) are different things. Page 03 reconciles
  all four, plus the tourism sub-total of 7,053. Quoting the largest as "tourists" overstates
  it 5.3-fold.

**Two gaps corrected on 13 September 2026.** The JNTO exports supersede Gap 03 — JNTO *does*
hold a named Pakistan series — and part of Gap 04, since an average length of stay is published.
What remains true, and is what Proposal 02 now rests on, is that Pakistan appears in no
*published* JNTO market breakdown. The correction is stated openly on pages 03 and 08 rather
than quietly folded in.

And two items still flagged as **confirm before presenting**: the transposed trade-direction
labels on MOFA's English basic-data page, and the undated end of the PIA Tokyo route.

---

## Updating the data

`data.py` and `jnto_data.py` are generated, not hand-written. After a source refresh, regenerate
them and then run the verification pass:

```bash
python verify.py
```

It recomputes every headline figure (shares, ratios, growth rates, totals) from the embedded data
and prints a pass/fail line for each. All 52 pass as shipped — including the two cross-checks
that validate the JNTO export corrections against independent sources.

---

## Notes on the design

The palette is inherited from the printed source catalogue and was validated for colour-vision
deficiency: worst adjacent-pair ΔE 9.9 (OKLab ×100, target ≥ 8), normal-vision floor 19.3
(≥ 15), every series above 3:1 contrast on white. The theme is pinned to light in
`config.toml` so a projector, a colleague's dark-mode laptop and a PDF export all show the same
thing. Web fonts (Zilla Slab, Source Sans 3, IBM Plex Mono, Noto Sans JP) load from Google Fonts;
offline, the app falls back to Georgia, the system sans and Hiragino for Japanese, and the layout
is unchanged.

## A note on the JNTO export

Two rows in JNTO's age-and-sex export — "Total" and "70 -" — belong to two different age
groupings and are emitted once per grouping, so they arrive at exactly twice their true value.
`jnto_data.py` halves them. The correction is validated two ways: after halving, the age bands
sum to 30,333 for 2024, which equals both the port-of-entry total in the companion file and the
separate from-chart export; and the 2019 total of 23,709 equals the Immigration Services Agency
all-entrants figure in the source workbook, to the person. Both checks run in `verify.py`.

Compiled 10 September 2026 from `Pakistan-Japan-Travel-Data.xlsx`; JNTO data added
13 September 2026 from statistics.jnto.go.jp.
