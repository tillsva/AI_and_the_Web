import streamlit as st
import random

st.header("Guessing Game")

# create a new random number if we don't have one yet
if "number" not in st.session_state:
    st.session_state["number"] = random.randint(1,100)
    st.info("New number generated!")

with st.form("number_form"):
    guess = st.number_input(
        "Enter a number",
        min_value=0,
        max_value=100,
        value=10,
        step=1,
    )
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(f"You submitted: {guess}")
    # Run your calculation or other action here.
    if guess == st.session_state['number']:
        st.success("Yeah! You did it")
        del st.session_state['number']
    else:
        st.error("Oh no. The number is wrong.")
        st.info(f"Debug info: The number is {st.session_state['number']}")
