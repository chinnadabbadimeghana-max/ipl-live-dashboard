# 🏏 IPL Data Analytics Project

Interactive IPL dashboards built on **295,732 ball-by-ball records** (1,243 matches, 2008 to 2026).

**🔗 Live demo:** https://chinnadabbadimeghana-max.github.io/ipl-live-dashboard/

## Dashboards
| Dashboard | What it shows |
|---|---|
| **Live Match Replay** | Ball-by-ball replay of 500+ real matches (all playoffs, 2023 to 2026 seasons, all RCB matches). Live scoreboard, win probability, worm chart, runs per over, run-source donut, batters and bowler stats, fall of wickets, match summary, 4 / 6 / wicket effects, speed control 1x to 10x, season and team filters |
| **Season Analysis** | Year-wise (2008 to 2026) tournament winner, total runs / wickets / 6s / 4s, Orange and Purple Cap, batsman and bowler selectors, toss impact, top 5 batsmen and bowlers, top winning teams, Player of the Match |

## Tech stack
- **Python (pandas):** data cleaning and aggregation (`clean_ipl.py`)
- **HTML, CSS, JavaScript** and **Chart.js** for the dashboards
- Hosted on **GitHub Pages**

## Data cleaning highlights
- Standardised franchise renames (Delhi Daredevils to Delhi Capitals, Kings XI Punjab to Punjab Kings, Royal Challengers Bangalore to Bengaluru)
- Merged duplicate stadium names (60 to 37 venues) and normalised seasons (`2007/08` to `2008`)
- Added analysis columns: `total_runs`, `is_wicket`, `is_legal_ball`, `phase` (Powerplay / Middle / Death), `is_four`, `is_six`, `ball_seq`
- Removed rain-affected (DLS) and no-result matches from the replay so targets are accurate
- Kept super-over balls out of the replay (innings 3+)

## Data source
[IPL Complete Dataset (2008 - 2026)](https://www.kaggle.com/) on Kaggle (`ipl_match_info_data.csv` and `ipl_match_ball_by_ball_data.csv`). The raw data is not included here; download it from Kaggle and run:
```bash
pip install pandas
python clean_ipl.py
```

## Notes
- Win probability in the replay is a simple estimated model (next step: logistic regression trained on this dataset).
- Unofficial fan project for learning and portfolio use. Team logos belong to their respective owners.
