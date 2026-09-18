import pandas as pd

df = pd.read_csv("Scouting_Database.csv")

#I want to drop the columns that have 100% missing values 
df = df.dropna(how="all", axis=1)


#Then i will convert minutes played to numeric first before removing the players who have played 0 minutes
df["playing time_min"] = pd.to_numeric(df["playing time_min"], errors="coerce").fillna(0)

#Then i will remove the rows where minutes played is 0
df = df[df["playing time_min"] > 0].copy()

#Then hapa i will fill the missing league values through mapping or forward fill/backward fill
if "league" in df.columns and "team" in df.columns:
    df["league"]=df.groupby("team")["league"].ffill().bfill()
    df["league"] = df["league"].fillna("Unknown")


#for the nation column i will still use the bfill and ffill then the remaining ones i can fill them with unknown

if "nation" in df.columns and "player" in df.columns:
    df["nation"]=df.groupby("player")["nation"].ffill().bfill()
    df["nation"] = df["nation"].fillna("Unknown")


#I'm going to drop the rows that have missing values in the age and born column. because they're basically useless to me. There are literally just 5 missing values 

#BTW I KNOW THAT BECAUSE I'VE CHECKED USING GOOGLE COLAB NOTEBOOK, WHERE I WAS ACTUALLY ABLE TO CLEAN THE DATA PROPERLY 
#HERE I'M JUST PUTTING THE CODE INTO ONE PLACE
if "age" in df.columns and "born" in df.columns:
    df = df.dropna(subset=["age", "born"])


#now i will fill the remaining numeric columns with 0
numeric_cols = df.select_dtypes(include='number').columns
df[numeric_cols] = df[numeric_cols].fillna(0.0)

print(df.isna().sum().sum())

df.to_csv("Scouting_Database_Cleaned.csv",index=False)
print("\nSuccess! Saved to 'Scouting_Database_Cleaned.csv' on your local computer.")
