import streamlit as st
import random
st.title("🎮Game play")
st.write("The guessing game will be started with a single click")

# Start a new gameif none is running.
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 100)
    st.session_state.guesses = 0
    st.session_state.won = False
    st.session_state.messages = [
        {"role": "assistant", "content": "I am thinking of a number between 1 and 100. can you guess it?"}
    ]
def evaluate(text):
#Check the users guess and return a message.
    try:
        number = int(text)
    except ValueError: # e.g hello, 6.8
        return "This is not a whole number. Please type a number like 25."
    if not 1 <= number <= 100:  
        return "Please guess a number between 1 and 100."

    st.session_state.guesses += 1
    if number < st.session_state.secret:
        return "Your guess is too low. Try again."
    if number > st.session_state.secret:
        return "Your guess is too high. Try again."

    # correct guess: end the game and save the results for the stats page

    st.session_state.won = True
    st.session_state.games.append(st.session_state.guesses)
    return f"🎉 Correct! the number was {st.session_state.secret}. you needed the guesses {st.session_state.guesses}."

# show the whole chat history 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

#after win: offer a new game. otherwise wait for the next new game.
if st.session_state.won:
    if st.button("start a new game"):
        del st.session_state.secret # next run starts a new game.
        st.rerun()
elif guess := st.chat_input("type your guess here"):
    st.session_state.messages.append({"role": "user", "content": guess})
    st.session_state.messages.append({"role": "assistant", "content": evaluate(guess)})
    st.rerun()