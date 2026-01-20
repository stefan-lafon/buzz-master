import streamlit as st
import random
from gtts import gTTS
import io
import base64

# Only capitalize the first letter of the title.
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
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["file_not_found"]

# Initialize session variables.
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
if "audio_to_play" not in st.session_state:
    st.session_state.audio_to_play = None

st.title("Buzz master")

# Stats displayed at the top.
col1, col2 = st.columns(2)
col1.metric("Correct", st.session_state.correct)
col2.metric("Misses", st.session_state.missed)

# This handles the audio queue.
if st.session_state.audio_to_play:
    play_audio(st.session_state.audio_to_play)
    st.session_state.audio_to_play = None

if st.button("🔊 Hear word"):
    st.session_state.audio_to_play = st.session_state.current_word
    st.rerun()

# Use a form so 'Enter' works naturally.
with st.form(key="spelling_form", clear_on_submit=True):
    guess = st.text_input("Enter spelling:").strip()
    submit = st.form_submit_button("Check")
    
    if submit and guess:
        if guess.lower() == st.session_state.current_word.lower():
            st.session_state.correct += 1
            st.session_state.audio_to_play = "Correct!"
            st.success(f"Nice! {st.session_state.current_word} is correct.")
        else:
            st.session_state.missed += 1
            st.session_state.history.append(st.session_state.current_word)
            st.session_state.audio_to_play = "Incorrect."
            st.error(f"Wrong. The correct spelling was: {st.session_state.current_word}")
        
        # Pick a new word for the next turn.
        st.session_state.current_word = random.choice(st.session_state.word_list)
        st.rerun()

# List of words to look at again later.
if st.session_state.history:
    with st.expander("Words to review"):
        for w in sorted(set(st.session_state.history)):
            st.write(f"• {w}")

if st.button("Reset session"):
    st.session_state.correct = 0
    st.session_state.missed = 0
    st.session_state.history = []
    st.rerun()