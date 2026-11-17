import streamlit as st
import pandas as pd

#edgecase if somehow the stats page is visited at first
if "numbergames" not in st.session_state:   
    games=None
    questions=None
else: 
    games = st.session_state.numbergames
    questions = st.session_state.questionswon

st.title("📊Statistics")

#nothing to show yet: give a hint and stop a page here
if not games and not questions:
    st.info("No game has been played yet. Go to play and finish a game first.")
    st.stop()


st.write("Games played so far:", len(games))

if games:
    st.header("Number Game")
    #key numbers, show side by side
    col1, col2, col3 = st.columns(3)
    col1.metric("Games played", len(games))
    col2.metric("Average of guesses", f"{sum(games) / len(games):.1f}")
    col3.metric("Best Game", f"{min(games)} guesses")

    #bar chart of the number of guesses per game
    st.subheader("Guesses per Game")
    chart_data = pd.DataFrame({
        "Game": range(1, len(games) + 1),
        "Guesses": games
    }) 
    st.bar_chart(chart_data, x="Game", y="Guesses", use_container_width=True)

if questions:
    st.header("Questions")

    total_questions = len(questions)
    correct_answers = sum(questions)
    wrong_answers = total_questions - correct_answers
    success_rate = (correct_answers / total_questions) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Questions played", total_questions)
    col2.metric("Correct answers", correct_answers)
    col3.metric("Wrong answers", wrong_answers)
    col4.metric("Success rate", f"{success_rate:.1f}%")

    st.subheader("Correct vs. Wrong Answers")

    chart_data = pd.DataFrame({
        "Result": ["Correct", "Wrong"],
        "Questions": [correct_answers, wrong_answers]
    })

    st.bar_chart(
        chart_data,
        x="Result",
        y="Questions",
        use_container_width=True
    )   
