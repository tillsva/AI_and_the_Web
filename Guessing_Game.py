import streamlit as st
import random 
import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError
import json

#Till
#selects a random question and removes it from the list
def get_question():
    df = random.choice(st.session_state.questions)
    question = df["question"]
    answer = df["answer"]
    st.session_state.questions.remove(df)
    return question, answer

#saves the api key to a session state variable
def save_api_key():
    st.session_state.api_key = st.session_state.uos_api_key.strip()

#returns the client
def get_client():
    if not st.session_state.api_key:
        return None
    return OpenAI(
        base_url="https://litellm.uni-osnabrueck.de/v1",
        api_key=st.session_state.api_key
    )

#resets the corresponding state variables
def next_game():
    st.session_state.won = False
    if st.session_state.game_mode == "number":
        #For the new game: generate new number, reset the won state and rerun the site
        st.session_state.number = random.randint(1, 100)
        st.session_state.guesses = 0
        st.session_state.number_messages = [
            {"role": "assistant", "content": "I am thinking of a number between 1 and 100. Can you guess it?"}
        ]
    else:
        st.session_state.terminate = False
        st.session_state.won = False
        st.session_state.question, st.session_state.answer = get_question()
        st.session_state.question_messages = [
            {"role": "assistant", "content": st.session_state.question}
        ]

#Sarmad
def evaluate_number(guess, number):
#Check the users guess and return a message.
    if not 1 <= guess <= 100:  
        return "Please guess a number between 1 and 100.", False
    print(st.session_state.number)
    st.session_state.guesses += 1
    if guess < number:
        return "Your guess is too low. Try again.", False
    if guess > number:
        return "Your guess is too high. Try again.", False

    # correct guess: end the game and save the results for the stats page
    
    st.session_state.won = True
    st.session_state.numbergames.append(st.session_state.guesses)
    return f"🎉 Correct! the number was {number}. you needed the guesses {st.session_state.guesses}.", True

#Abhi
def evaluate_questions(input, answer, question):
    cleaned_input = input.lower()
    cleaned_answer = answer.lower()

    if cleaned_answer==cleaned_input:
        return True

    prompt = f"""
    You are an evaluator for a guessing game. Compare the user's answer to the correct answer.
    
    Question: "{question}"
    Correct Answer: "{cleaned_answer}"
    User's Answer: "{cleaned_input}"

    Task: Determine if the user's answer semantically matches the correct answer.
    - Ignore minor misspellings or typos.
    - Pay close attention to polarity: If the correct answer is "no", words like "yes", "for sure", "definitely", or "yep" do NOT match and must be False.
    - Output ONLY the word "True" or "False". No explanation.
    """

    messages = [{"role": "user", "content": prompt}]

    try:
        with st.spinner("Answer is evaluated …"):
            response = client.chat.completions.create(
                model="google/gemma-4-E4B-it",
                messages=messages,
                temperature=0.0
                )
        
        result = response.choices[0].message.content.strip().lower()
        if result == "true":
            return True
        else:
            return False
        
    except AuthenticationError:
        st.error("API was not accepted. Please check it.")
        return None

    except OpenAIError:
        st.error(
            "AI API request failed. Please check it and try again. "
        )
        return None

st.set_page_config(
    page_title="Guessing Game",
    page_icon="🎯"
)

st.write("# Welcome to the guessing game!")

#Init session variables, if no game is running
#Sarmad/Till
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 100)
    st.session_state.guesses = 0
    st.session_state.won = False
    st.session_state.game_mode = "number"
    st.session_state.numbergames = []
    st.session_state.msg = ""
    st.session_state.terminate = False
    st.session_state.api_key = ""
    st.session_state.questionswon = []
    st.session_state.number_input = 50
    st.session_state.number_messages = [
        {"role": "assistant", "content": "I am thinking of a number between 1 and 100. Can you guess it?"}
    ]
    st.session_state.question_messages = []

    with open("general_knowledge_questions.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    st.session_state.questions = data.get("questions", [])

    st.session_state.question, st.session_state.answer = get_question()

#Init LLM by Abhi
# ── ask for API Key, stop if not yet provided  ────────────────────────────────────────────
with st.sidebar:
    st.subheader("Settings")
    st.session_state.api = st.text_input(
        "UOS AI API-Key",
        type="password",
        key="uos_api_key",
        on_change=save_api_key,
        placeholder="sk-...",
    ).strip()

#Two Columns for the two kinds of games
#Till
col1, col2 = st.columns(2)
with col1:
    if st.button(
        "Give me the odds",
        use_container_width=True,
        type="primary" if st.session_state.game_mode == "number" else "secondary"
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

#Sarmad
if st.session_state.game_mode == "number":
    st.header("Give me the odds")

    # Show the whole chat history
    for msg in st.session_state.number_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # After a win, offer a new game. Otherwise wait for the next guess.
    if st.session_state.won:
        if st.button("Start a new game"):
            next_game()
            st.rerun()
    elif guess := st.chat_input("Type your guess here"):
        st.session_state.number_messages.append({"role": "user", "content": guess})
        try:
            number_guess = int(guess)
        except ValueError:
            st.session_state.msg = "This is not a whole number. Please type a number like 25."
            won = False
        else:
            st.session_state.msg, won = evaluate_number(number_guess, st.session_state.number)
        st.session_state.number_messages.append({"role": "assistant", "content": st.session_state.msg})
        st.session_state.won = won
        st.rerun()

#Till
elif st.session_state.game_mode == "questions":
    # pass the entered key
    client = get_client()

    #stops if no api key is entered 
    if client is None:
        st.info("Please enter your UOS AI API key.")
        st.stop()

    st.header("Questions")
    if not st.session_state.question_messages:
        st.session_state.question_messages = [
            {"role": "assistant", "content": st.session_state.question}
        ]

    # Show the whole chat history
    for msg in st.session_state.question_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # After an answer, offer the next question. Otherwise wait for the next guess.
    if st.session_state.terminate:
        if st.button("Next Question"):
            if len(st.session_state.questions) > 0:
                next_game()
                st.rerun()
            else:
                st.success("All question answered! Well done!")
    elif guess := st.chat_input("Type your answer here"):
        st.session_state.question_messages.append({"role": "user", "content": guess})

        #Evaluate the question
        correct = evaluate_questions(guess, st.session_state.answer, st.session_state.question)

        #If correct, safe the corresponding message, set the terminate and won states and safe the result in the winning history
        if correct:
            st.session_state.msg = "Right!"
            st.session_state.terminate = True
            st.session_state.won = True
            st.session_state.questionswon.append(True)
            st.session_state.question_messages.append({"role": "assistant", "content": st.session_state.msg})
            st.rerun()

        #Explicitly asking for false for the case a error occurs and none is returned
        elif correct == False:
            st.session_state.msg = f"Wrong! The answer was {st.session_state.answer}!"
            st.session_state.terminate = True
            st.session_state.won = False
            st.session_state.questionswon.append(False)
            st.session_state.question_messages.append({"role": "assistant", "content": st.session_state.msg})
            st.rerun()
    


