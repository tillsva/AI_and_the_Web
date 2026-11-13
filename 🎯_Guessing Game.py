import streamlit as st
import random 
import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError
import sys

st.set_page_config(
    page_title="Guessing Game",
    page_icon="🎯"
)

st.write("# Welcome to the guessing game!")

if "game_mode" not in st.session_state:
    st.session_state.game_mode = "number"

if "number" not in st.session_state:
    st.session_state.number = None

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "Give me the odds",
        use_container_width=True,
        type="primary" if st.session_state.game_mode == "odds" else "secondary"
    ):
        st.session_state.game_mode = "number"
        st.rerun()
        
with col2:
    if st.button(
        "Questions",
        use_container_width=True,
        type="primary" if st.session_state.game_mode == "questions" else "secondary"
    ):
        st.session_state.game_mode = "questions"
        st.rerun()



if st.session_state.game_mode == "number":
    st.header("Give me the odds")
    st.write("Guess the randomly generated number!")

    number_range = st.slider(
    "Choose number range",
    min_value=1,
    max_value=1000,
    value=(1,100),
    step=1
    )

    min_number = number_range[0]
    max_number = number_range[1]

    if st.session_state.number is None:
        st.session_state.number = random.randint(min_number, max_number)

    with st.form("number_form"):

        guess = st.number_input(
            "Enter a number",
            min_value=min_number,
            max_value=max_number,
            value=10,
            step=1,
        )

        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("Submit")

        with col2:
            reset = st.form_submit_button("Reset")

        if reset:
            st.session_state.number = random.randint(min_number, max_number)

        if submit:
            if guess == st.session_state.number:
                st.success("Correct! You won!")
                st.balloons()
            else:
                st.warning(f"Wrong! The number was {st.session_state.number}!")

elif st.session_state.game_mode == "questions":
    st.header("Questions")

    question = "How many residents does Osnabrück have?"
    answer = 166277
    st.write(question)

    
    
    with st.form("number_form"):
    
        guess = st.number_input(
            "Enter a number",
            min_value=0,
            max_value=1000000,
            value=10,
            step=1,
        )
    
        col1, col2 = st.columns(2)
    
        with col1:
            submit = st.form_submit_button("Submit")
    
        with col2:
            next = st.form_submit_button("Next")
    
        if next:
            st.session_state.number = 166257
    
        if submit:
            if guess == answer:
                st.success("Correct! You won!")
                st.balloons()
            else:
                st.warning(f"Wrong! The number was {st.session_state.number}!")


st.set_page_config(page_title="Talk to AI", page_icon="🤖")
sys.stdout.reconfigure(encoding='utf-8')

# ── ask for API Key, stop if not yet provided  ────────────────────────────────────────────
with st.sidebar:
    api_key = st.text_input(
        "UOS AI API-Key",
        type="password",
        key="uos_api_key",
        placeholder="sk-...",
    ).strip()
how to 
if not api_key:
    st.info("Please enter your Uni Osnabrück API key. If you don't have one, you can obtain it from https://ai-keys.uni-osnabrueck.de.")
    st.stop()

# pass the entered key
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=api_key
)

# ── Main program logic starts here ────────────────────
st.title("Talk to AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.text_area("Your Question")

if st.button("Submit", disabled=not prompt.strip()):
    try:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Answer is being created …"):
            response = client.chat.completions.create(
                model="google/gemma-4-E4B-it",
                messages=st.session_state.messages,
            )

        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.write(answer)

    except AuthenticationError:
        st.error("API was not accepted. Please check it.")

    except OpenAIError:
        st.error(
            "AI API request failed. Please check it and try again. "
        )

#TODO s for me: 
#Implement a question database 
#Implement a username form and stats database 



