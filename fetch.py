import pandas as pd 
import soccerdata as sd


print("Initializing scraper...")

#This is a list of all the leagues that I want to scrape from
#I have included the big 5 European leagues as well as the mls as well as the brazilian league as well as the argentinian league as well as the saudi pro league
fbref = sd.FBref(
    leagues = ["Big 5 European Leagues Combined"], 
    seasons = ['2022-23','2023-24','2024-25','2025-26','2026-27'], 
    headless=False
    )

#This is where I am reading the data from the fbref object
#I am reading the data from the standard,possession,keepers,defense,gca,passing,and errors dataframes
#I am also resetting the index of the dataframes
df_standard = fbref.read_player_season_stats(stat_type="standard").reset_index()
df_shooting=fbref.read_player_season_stats(stat_type="shooting").reset_index()
df_keepers=fbref.read_player_season_stats(stat_type="keeper").reset_index()
df_playing_time=fbref.read_player_season_stats(stat_type="playing_time").reset_index()
df_misc = fbref.read_player_season_stats(stat_type="misc").reset_index()


def clean_columns(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip('_') for col in df.columns.values]
    df.columns = [str(col).lower() for col in df.columns]
    df = df.loc[:, ~df.columns.duplicated()].copy() #this is where i remove duplicate columns
    return df

df_standard=clean_columns(df_standard)
df_shooting=clean_columns(df_shooting)
df_keepers=clean_columns(df_keepers)
df_playing_time=clean_columns(df_playing_time)
df_misc = clean_columns(df_misc)

merge_keys = ["player", "league", "season", "pos", "team"] #this is where i define the columns that i want to merge the dataframes on

def merge_stats(left_df,right_df,df_keys):
    new_cols = [col for col in right_df.columns if col in df_keys or col not in left_df.columns] #this is where i get new columns
    
    merged_df = pd.merge( #this is where i merge the dataframes using the merge keys
        left_df,
        right_df[new_cols], 
        how="left", 
        on=df_keys,
        )
    return merged_df


df_outfield_std = df_standard[~df_standard["pos"].astype(str).str.contains("GK", na=False)].copy()
df_outfield_misc = df_misc[~df_misc["pos"].astype(str).str.contains("GK", na=False)].copy()
df_outfield_playing_time = df_playing_time[~df_playing_time["pos"].astype(str).str.contains("GK", na=False)].copy()
df_outfield_shooting = df_shooting[~df_shooting["pos"].astype(str).str.contains("GK", na=False)].copy()

outfield_dfs = [df_outfield_std,df_outfield_misc,df_outfield_playing_time,df_outfield_shooting]

df_master = outfield_dfs[0]
for df in outfield_dfs[1:]:
    df_master = merge_stats(df_master,df,merge_keys)


df_master.to_csv("Scouting_Database.csv",index=False)
print("\nSuccess! Saved to 'Scouting_Database.csv' on your local computer.")


#Now for the goalkeepers' csv 

df_gks = df_standard[df_standard["pos"].astype(str).str.contains("GK", na=False)].copy() #Here I am getting the Goalkeeper data from the df_standard dataframe

df_gks = merge_stats(df_gks,df_keepers,merge_keys) #tena sasa nimerge df_gks na df_keepers

df_gks.to_csv("Scouting_GKs.csv",index=False)
print("\nSuccess! Saved to 'Scouting_GKs.csv' on your local computer.")
