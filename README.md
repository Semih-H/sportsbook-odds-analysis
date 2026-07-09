# Sportsbook Market Analysis — Top-5 European Leagues, 2025

Closing-odds market analysis of 1,736 matches (Premier League, La Liga,
Bundesliga, Serie A, Ligue 1, calendar year 2025), built as an
end-to-end pipeline: two independent data sources, validated join,
statistical analysis, and an interactive Tableau dashboard.

**Dashboard:** [Tableau Public — Sportsbook Market Analysis 2025](YOUR-URL)

## Key findings
- **Sharp vs retail margins:** Pinnacle prices a near-constant ~3.0%
  overround in every league; Bet365 averages ~5.6%. Retail margins
  compress to 4.8% in the Premier League — the most liquid market —
  a large, significant effect (Welch t = −13.8, Cohen's d = −0.79).
- **Margins were stable all year.** An apparent rising trend in the
  market-average margin turned out to be a composition artifact of the
  source's bookmaker panel changing between seasons — single-book
  series are flat. (See data quality log.)
- **Favorite–longshot bias, quantified in money:** flat-stake bets on
  longshots (<15% implied) lost 34% at Pinnacle and 44% at Bet365 in
  2025; heavy favorites (>75%) broke even or better at both books.
  The bookmaker's edge is extracted almost entirely from longshot
  and mid-range backers.

## Pipeline
API (football-data.org) ─┐
                         ├─ pandas cleaning & entity resolution ─ EDA ─ Tableau exports
CSVs (football-data.co.uk) ┘

- `src/ingest_api.py` — match results via REST API (auth, rate limiting, raw-layer JSON)
- `src/ingest_csv.py` — closing odds CSVs (see acquisition notes below)
- `notebooks/01_cleaning.ipynb` — schema-drift audit, keep-list decisions,
  team-name mapping table, join validated to 100% with cross-source score checks
- `notebooks/02_eda.ipynb` — margins, calibration, flat-stake P&L, statistical tests
- `data/processed/` — final tidy tables consumed by Tableau

## Data quality log
Issues found and resolved during the build:
1. Stale local file masquerading as current data — caught by file-date
   and row-count inspection before analysis.
2. William Hill and Bwin odds dropped: coverage gaps of 62% / 71%
   inside the analysis window, diagnosed to the month.
3. Pinnacle retained after temporal analysis showed its missing block
   lay entirely outside the 2025 window.
4. Two computation traps: pandas `sum(skipna=True)` fabricating a −100%
   overround on a missing-odds row; a source-side aggregate error
   producing an impossible "arbitrage" on one match (aggregates voided,
   match kept).
5. The composition artifact in finding #2 above.

## Acquisition notes
football-data.co.uk rejects non-browser TLS fingerprints on some
networks; the ingestion script is retained as the canonical acquisition
path, with files browser-acquired where the block applies. Regional
network restrictions were also encountered and documented.

## Reproducing
conda env create -f environment.yml, add a football-data.org key to
.env (see .env.example), run the two ingest scripts, then the notebooks
in order.