import streamlit as st
import pandas as pd

st.title("📊statistics")
st.write("games played so far:", len(st.session_state.games))

games = st.session_state.games

#nothing to show yet: give a hint and stop a page here
if not games:
    st.info("no game has been played yet. Go to play and finish a game first.")
    st.stop()

#key numbers, show side by side
col1, col2, col3 = st.columns(3)
col1.metric("games played", len(games))
col2.metric("Average of guesses", f"{sum(games) / len(games):.1f}")
col3.metric("best game", f"{min(games)}guesses")

#bar chart of the number of guesses per game
st.subheader("Guesses per game")
chart_data = pd.DataFrame({
    "Game": range(1, len(games) + 1),
    "Guesses": games
}) 
st.bar_chart(chart_data, x="Game", y="Guesses", use_container_width=True)