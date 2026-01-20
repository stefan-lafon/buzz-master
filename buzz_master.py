import streamlit as st
import random
from gtts import gTTS
import io
import base64

# Simple title formatting as requested.
st.set_page_config(page_title="Buzz master", page_icon="🐝")

def play_audio(text):
    """Generates and injects an audio player that starts immediately."""
    tts = gTTS(text=text, lang='en')
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    b64_audio = base64.b64encode(audio_buffer.read()).decode()
    audio_html = f'<audio autoplay src="data:audio/mp3;base64,{b64_audio}">'
    st.markdown(audio_html, unsafe_allow_html=True)

def load_words():
    """Reads the word list from the local file."""
    try:
        with open("words.txt", "r") as f:
            # Strip whitespace and ignore empty lines.
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["wordfile_missing"]

# Set up the session variables so data persists across refreshes.
if "word_list" not in st.session_state:
    st.session_state.word_list = load_words()
if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(st.session_state.word_list)
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "missed" not in st.session_state:
    st.session_state.missed = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "feedback" not in st.session_state:
    st.session_state.feedback = None

st.title("Buzz master")

# Scoreboard row.
col1, col2 = st.columns(2)
col1.metric("Correct", st.session_state.correct)
col2.metric("Misses", st.session_state.missed)

st.write("Press the button to hear the word.")

if st.button("🔊 Hear word"):
    play_audio(st.session_state.current_word)

# Form for user input.
with st.form(key="spelling_form", clear_on_submit=True):
    guess = st.text_input("Type the word here:").strip()
    submit = st.form_submit_button("Check spelling")
    
    if submit and guess:
        if guess.lower() == st.session_state.current_word.lower():
            st.session_state.feedback = ("success", f"Nice! {st.session_state.current_word} is correct.")
            st.session_state.correct += 1
        else:
            st.session_state.feedback = ("error", f"Not quite. The correct spelling was: {st.session_state.current_word}")
            st.session_state.missed += 1
            # Add missed words to a list for later review.
            st.session_state.history.append(st.session_state.current_word)
        
        # Pick a new word immediately for the next round.
        st.session_state.current_word = random.choice(st.session_state.word_list)
        st.rerun()

# Display feedback from the previous attempt if it exists.
if st.session_state.feedback:
    style, msg = st.session_state.feedback
    if style == "success":
        st.success(msg)
    else:
        st.error(msg)

# Review section for missed words.
if st.session_state.history:
    with st.expander("Review missed words"):
        # Show unique words missed.
        for w in sorted(set(st.session_state.history)):
            st.write(f"• {w}")

if st.button("Clear session"):
    st.session_state.correct = 0
    st.session_state.missed = 0
    st.session_state.history = []
    st.session_state.feedback = None
    st.rerun()