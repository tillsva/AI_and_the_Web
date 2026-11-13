import streamlit as st

st.set_page_config(page_title="Guessing Game", page_icon="🎯")

if "games" not in st.session_state:
    st.session_state.games = []

page = st.navigation([
      st.Page("play.py", title="play", icon="🎮"),
      st.Page("stats.py", title="stats", icon="📊"), 
    ])
    
page.run()