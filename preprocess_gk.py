import pandas as pd

print("1. Loading cleaned Goalkeepers database...")
df_gk = pd.read_csv("Scouting_GKs_Cleaned.csv")

df_gk["season"] = 2000 + (df_gk["season"]//100)

# FILTER LOW-MINUTE GOALKEEPERS (900+ Total Mins)
df_gk["total_career_mins"] = df_gk.groupby("player")["playing time_min"].transform("sum")
df_gk = df_gk[df_gk["total_career_mins"] >= 900].copy()

# DEFINE GOALKEEPER COLUMNS TO AGGREGATE
# Raw counting stats to SUM across seasons
gk_raw_stats = [
    "performance_ga", 
    "performance_sota", 
    "performance_saves", 
    "performance_cs",
    "penalty kicks_pksv"
]

# Existing percentage/rate stats to AVERAGE across seasons
gk_rate_stats = [
    "performance_save%", 
    "performance_cs%",
    "penalty kicks_save%"
]

# Filter list to keep only existing columns
gk_raw_stats = [col for col in gk_raw_stats if col in df_gk.columns]
gk_rate_stats = [col for col in gk_rate_stats if col in df_gk.columns]


# STEP 3: AGGREGATE STATS INTO 1 ROW PER GOALKEEPER
agg_dict = {
    "team": "last",
    "league": "last",
    "pos": "last",
    "nation": "last",
    "age": "last",
    "playing time_min": "sum"
}

# Add SUM rule for raw counts
for col in gk_raw_stats:
    agg_dict[col] = "sum"

# Add MEAN rule for percentage rates
for col in gk_rate_stats:
    agg_dict[col] = "mean"

df_gk_player = df_gk.groupby("player").agg(agg_dict).reset_index()

#CONVERT RAW TOTALS TO CAREER PER-90s
for col in gk_raw_stats:
    df_gk_player[col + "_per90"] = (df_gk_player[col] / df_gk_player["playing time_min"]) * 90

final_cols = (
    ["player", "team", "league", "pos", "nation", "age", "playing time_min"]
    + gk_rate_stats
    + [col + "_per90" for col in gk_raw_stats]
)

df_gk_final = df_gk_player[final_cols].copy()

# Save final processed file
df_gk_final.to_csv("gk_processed.csv", index=False)
print(f"Success! Saved 'gk_processed.csv' with {len(df_gk_final)} unique goalkeepers!")