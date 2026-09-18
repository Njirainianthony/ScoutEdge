import pandas as pd

print("1. Loading raw Goalkeepers database...")
df_gk = pd.read_csv("Scouting_GKs.csv")

# 1. Drop 100% empty columns (if any)
df_gk = df_gk.dropna(how="all", axis=1)

# 2. Convert minutes played to numeric and filter out 0-minute rows
df_gk["playing time_min"] = pd.to_numeric(df_gk["playing time_min"], errors="coerce").fillna(0)
df_gk = df_gk[df_gk["playing time_min"] > 0].copy()

# 3. Map missing league and nation using team/player history
if "league" in df_gk.columns and "team" in df_gk.columns:
    df_gk["league"] = df_gk.groupby("team")["league"].ffill().bfill()
    df_gk["league"] = df_gk["league"].fillna("Unknown")

if "nation" in df_gk.columns and "player" in df_gk.columns:
    df_gk["nation"] = df_gk.groupby("player")["nation"].ffill().bfill()
    df_gk["nation"] = df_gk["nation"].fillna("Unknown")

# 4. Drop rows missing age or born year
if "age" in df_gk.columns and "born" in df_gk.columns:
    df_gk = df_gk.dropna(subset=["age", "born"]).copy()

# 5. Fill ratio/percentage NaNs (like save%, cs%, penalty save%) with 0.0
numeric_cols = df_gk.select_dtypes(include='number').columns
df_gk[numeric_cols] = df_gk[numeric_cols].fillna(0.0)

print(f"Total remaining NaNs in Goalkeeper dataset: {df_gk.isna().sum().sum()}")

# Save clean checkpoint
df_gk.to_csv("Scouting_GKs_Cleaned.csv", index=False)
print("Success! Saved 'Scouting_GKs_Cleaned.csv'")