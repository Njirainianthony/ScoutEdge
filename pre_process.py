import pandas as pd

df = pd.read_csv("Scouting_Database_Cleaned.csv")


#First i will correct the seasons column e.g instead of 2223 season I'll just put the first year of that season. So instead of 2223 it will be 2022
df["season"] = 2000 + (df["season"]//100)

#Here i am going to calculate the total number of minutes played by each player
#then i am going to remove players who have played less than 900 minutes

df["Total_Minutes"] = df.groupby("player")["playing time_min"].transform("sum")

df = df[df["Total_Minutes"]>=900].copy()

#Here i am going to do some feature selection 

raw_stat_cols = [
    'performance_gls', 'performance_ast', 'performance_g-pk', 
    'performance_pk', 'performance_crdy', 'performance_crdr',
    'performance_fls', 'performance_fld', 'performance_off',
    'performance_crs', 'performance_int', 'performance_tklw',
    'standard_sh', 'standard_sot'   
]

# These are the metrics that i will be required to do the average across the seasons

rate_cols = ['standard_sot%', 'standard_g/sh', 'team success_ppm']

#These will be the metadata columns to keep because it would be useless to have the metrics but do not know which players to look for 
meta_cols = ['player', 'team', 'league', 'age', 'nation', 'pos', 'playing time_min']

#this one is to filter list to make sure columns exist in our csv
raw_counting_stats = [col for col in raw_stat_cols if col in df.columns]
raw_rate_stats = [col for col in rate_cols if col in df.columns]
raw_meta_stats = [col for col in meta_cols if col in df.columns]

#Now i am going  to aggregate the stats for each player

agg_dict = {
    "team": "last",
    "league": "last",
    "age": "last",
    "nation": "last",
    "pos": "last",
    "playing time_min": "sum",
    "season": "last" #nimeongeza hii so that it can pick the latest season that player played
}

#now here I am going to do sum for the raw cols
for col in raw_counting_stats:
    agg_dict[col] = "sum"

#mean for rate stats
for col in raw_rate_stats:
    agg_dict[col] = "mean"

#Now i'll group by player and apply the calculations
df_player = df.groupby("player").agg(agg_dict).reset_index()

#Sasa hapa ndio I will convert the raw totals to per 90s 
for col in raw_counting_stats:
    df_player[col + "_per90"] = df_player[col]/df_player["playing time_min"] * 90

final_cols = meta_cols + raw_rate_stats + [col + "_per90" for col in raw_counting_stats]

df_final = df_player[final_cols].copy() #so this is the new and final dataframe that we have in order to make our model

df_final.to_csv("Scouting_Database_Final.csv",index=False)
print(len(df_final))

print("\nSuccess! Saved to 'Scouting_Database_Final.csv' on your local computer.")
