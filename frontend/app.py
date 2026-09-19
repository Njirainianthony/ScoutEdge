import streamlit as st 
import requests

st.set_page_config(page_title="ScoutEdge", page_icon="⚽", layout="wide")

st.title("ScoutEdge ⚽: Your AI Powered Scouting Engine")
st.markdown("Find the best young players for your team!")

API_URL = "https://scoutedge-91u0.onrender.com"

st.sidebar.header("About")
st.sidebar.info("ScoutEdge is a web application that helps football clubs find the best young players for their teams.")

st.sidebar.header("How it works")
st.sidebar.info("ScoutEdge uses machine learning to find the best young players for your team.")

st.sidebar.header("Scouting Settings")
position_type = st.sidebar.radio("Select Player Position",["outfield", "gk"])
top_n = st.sidebar.slider("Number of Similar Players", min_value=3, max_value=15,value=5)

#Search bar
player_query = st.text_input("Enter Player Name:")

if st.button("Search") or player_query:
    formatted_position = str(position_type).lower()
    
    if not player_query.strip():
        st.warning("Please enter a player name")
    
    else:
        with st.spinner("Querying AI ScoutEdge..."):
            try:
                response = requests.get(
                    f"{API_URL}/similar/{player_query}",
                    params = {"position_type": formatted_position, "top_n": top_n}
                )

                if response.status_code ==200:
                    data = response.json()

                    st.success("Found players!")

                    st.subheader(f"Similar Players to {data['player']}")
                    clones = data.get("top_matches") or data.get("top_similar_players") or data.get("clones") or data.get("matches")

                    st.dataframe(
                        clones,
                        use_container_width=True,
                        column_config={
                            "player": "Player",
                            "team": "Team",
                            "league": "League",
                            "position": "Pos",
                            "age": "Age",
                            "nation": "Nation",
                            "playing_time_min": "Career Mins",
                            "similarity_score": "Match Score"
                        }
                    )
                    
                elif response.status_code == 404:
                    st.error("Player not found")
                else:
                    st.error("Server error occurred")
                
            except requests.exceptions.ConnectionError:
                st.error("Backend Server is down. Please check if it is running.")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
                
                




                
            
            

