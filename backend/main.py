from fastapi import FastAPI, HTTPException # fastapi is a python framework for building APIs, httpexception is used to raise HTTP errors (it's like a built in error handler)
import pickle #this is just used to load the trained model here
import pandas as pd
import unicodedata #this one is used to clean the names, removing those accents so that the similarity search works properly
import difflib #this one is used to find the closest matching name

app = FastAPI(title = "ScoutEdge", description = "Soccer player similarity search engine")

#Here is where i load my model artifacts
with open ("model_artifacts_outfield.pkl", "rb") as f:
    outfield_model = pickle.load(f)


with open("gk_model_artifacts.pkl", "rb") as f:
    gk_model = pickle.load(f)


#now this is where i clean the name by removing the accents so that the user does not have any problems when using the system
def clean_str(text:str) -> str:
    return unicodedata.normalize('NFD', str(text)).encode('ascii','ignore').decode('utf-8').strip().lower()


@app.get("/")
def home():
    return {
        "message": "Welcome to ScoutEdge!"
    }


@app.get("/similar/{player_name}") #this is where i define the endpoint for the similarity search
def search_similar(player_name:str, position_type:str="outfield", top_n:int=10):
    model = outfield_model if position_type == "outfield" else gk_model

    df = model["df"] #this is where i load the dataframe
    sim_matrix = model["similarity_matrix"] #this is where i load the similarity matrix

    db_clean_names = df["player"].apply(clean_str).tolist() #this is where i get the cleaned names of the players in the database
    query_clean = clean_str(player_name) #this is where i get the cleaned name of the player that the user searched for
    matches = difflib.get_close_matches(query_clean, db_clean_names, n=1, cutoff=0.6) #this is where i find the closest matching name

    if not matches: #this is where i check if the player was found
        raise HTTPException(status_code=404, detail="Player '{player_name}' not found ")

    matched_name = db_clean_names.index(matches[0]) #this is where i get the index of the matched name
    target_player =df.iloc[matched_name] #this is where i get the target player's data

    df_temp = df.copy() #this is where i make a copy of the dataframe
    df_temp['similarity_score'] = sim_matrix[matched_name] #this is where i add the similarity scores to the dataframe

    results = df_temp.nlargest(top_n+1, "similarity_score").iloc[1:].copy() #this is where i get the top n similar players, but I'll skip the first one because the first one is just the player himself

    clones = [] #this is an empty list where I will store the similar players
    for _, row in results.iterrows(): #this is where i iterate through the similar players
        clones.append({
            "player": str(row["player"]),
            "age": int(row["age"]),
            "nation": str(row["nation"]),
            "pos": str(row["pos"]),
            "league": str(row["league"]),
            "team": str(row["team"]),
            "similarity_score": f"{round(row['similarity_score']*100, 2)}%"
        })

    return{
        "player": str(target_player["player"]), #this is where i get the target player's data
        "age": int(target_player["age"]),
        "nation": str(target_player["nation"]),
        "pos": str(target_player["pos"]),
        "league": str(target_player["league"]),
        "team": str(target_player["team"]),
        "top_matches": clones
    }