"""IPL data cleaning. Put this file in the same folder as the 2 raw CSVs and run: python clean_ipl.py"""
import pandas as pd

RAW_B, RAW_M = "ipl_match_ball_by_ball_data.csv", "ipl_match_info_data.csv"
b = pd.read_csv(RAW_B, low_memory=False)
m = pd.read_csv(RAW_M)

# ---------- 1. Standardize team names (franchise renames) ----------
TEAMS = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
}
for df, cols in ((m, ["team1", "team2", "toss_winner", "winner"]), (b, ["batting_team", "bowling_team"])):
    for c in cols:
        df[c] = df[c].replace(TEAMS)

# ---------- 2. Standardize venues (same stadium written 2-3 ways) ----------
VENUE_ALIAS = {
    "Feroz Shah Kotla": "Arun Jaitley Stadium",
    "M.Chinnaswamy Stadium": "M Chinnaswamy Stadium",
    "Punjab Cricket Association Stadium": "Punjab Cricket Association IS Bindra Stadium",
    "Sardar Patel Stadium": "Narendra Modi Stadium",
    "Sheikh Zayed Stadium": "Zayed Cricket Stadium",
}
def clean_venue(v):
    v = str(v).split(",")[0].strip()
    return VENUE_ALIAS.get(v, v)
m["venue"] = m["venue"].map(clean_venue)
b["venue"] = b["venue"].map(clean_venue)

# ---------- 3. Season -> single year (2007/08 -> 2008, 2009/10 -> 2010, 2020/21 -> 2020) ----------
SEASON = {"2007/08": 2008, "2009/10": 2010, "2020/21": 2020}
for df in (m, b):
    df["season"] = df["season"].map(lambda s: SEASON.get(s, s)).astype(int)

# ---------- 4. Matches table ----------
m["date"] = pd.to_datetime(m["date"])
m["winner"] = m["winner"].fillna("No Result")
m["player_of_match"] = m["player_of_match"].fillna("N/A")
m["city"] = m["city"].fillna(m.groupby("venue")["city"].transform("first"))  # fill from same venue
m = m.drop(columns=["date_1", "reserve_umpire", "tv_umpire", "gender", "event"])

# ---------- 5. Ball-by-ball table ----------
b["start_date"] = pd.to_datetime(b["start_date"])
for c in ["wides", "noballs", "byes", "legbyes", "penalty"]:
    b[c] = b[c].fillna(0).astype(int)           # NaN just means "no such extra"
b = b.drop(columns=["other_wicket_type", "other_player_dismissed"])  # 100% empty
b["total_runs"] = b["runs_off_bat"] + b["extras"]
# retired hurt/out are not bowler wickets
b["is_wicket"] = (b["player_dismissed"].notna() & ~b["wicket_type"].isin(["retired hurt", "retired out"])).astype(int)
b["is_legal_ball"] = ((b["wides"] == 0) & (b["noballs"] == 0)).astype(int)
b["over"] = b["ball"].astype(int)                       # 0..19
b["is_four"] = (b["runs_off_bat"] == 4).astype(int)
b["is_six"] = (b["runs_off_bat"] == 6).astype(int)
b["is_super_over"] = (b["innings"] > 2).astype(int)     # innings 3+ = super over
b["phase"] = pd.cut(b["over"], [-1, 5, 15, 99], labels=["Powerplay", "Middle", "Death"])
b["ball_seq"] = b.groupby(["match_id", "innings"]).cumcount() + 1   # order of delivery, used for live replay

# NOTE: 3 "duplicate-looking" rows are real (e.g. two wides on the same ball number), so we do NOT drop them.

m.to_csv("matches_clean.csv", index=False)
b.to_csv("deliveries_clean.csv", index=False)
print("matches:", m.shape, "| deliveries:", b.shape)
print("teams:", sorted(set(m.team1) | set(m.team2)))
print("venues:", m.venue.nunique(), "| seasons:", sorted(m.season.unique()))
