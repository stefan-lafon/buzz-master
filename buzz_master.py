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

# Initialize session state for persistent data.
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
if "session_started" not in st.session_state:
    st.session_state.session_started = False
if "audio_to_play" not in st.session_state:
    st.session_state.audio_to_play = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.title("Buzz master")

# Stats displayed at the top.
col1, col2 = st.columns(2)
col1.metric("Correct", st.session_state.correct)
col2.metric("Misses", st.session_state.missed)

# Handle the voice feedback or automatic word play.
if st.session_state.audio_to_play:
    play_audio(st.session_state.audio_to_play)
    # We clear it so it doesn't loop on every minor interaction.
    st.session_state.audio_to_play = None

st.divider()

# Logic for starting the session.
if not st.session_state.session_started:
    st.write("Welcome to the training session. Ready to begin?")
    if st.button("Start session"):
        st.session_state.session_started = True
        st.session_state.audio_to_play = st.session_state.current_word
        st.rerun()

# Only show the game once the session has started.
elif st.session_state.last_result:
    res_type, res_text = st.session_state.last_result
    if res_type == "correct":
        st.success(f"### {res_text}")
    else:
        st.error(f"### {res_text}")
    
    if st.button("Move to next word"):
        st.session_state.last_result = None
        st.session_state.current_word = random.choice(st.session_state.word_list)
        st.session_state.audio_to_play = st.session_state.current_word
        st.rerun()
else:
    # Practice mode.
    st.write(f"Word length: **{len(st.session_state.current_word)} letters**")
    
    if st.button("🔊 Re-play word"):
        st.session_state.audio_to_play = st.session_state.current_word
        st.rerun()

    with st.form(key="spelling_form", clear_on_submit=True):
        guess = st.text_input("Type your spelling:").strip()
        submit = st.form_submit_button("Submit answer")
        
        if submit and guess:
            if guess.lower() == st.session_state.current_word.lower():
                st.session_state.correct += 1
                st.session_state.audio_to_play = "Correct!"
                st.session_state.last_result = ("correct", "Correct! Well done.")
            else:
                st.session_state.missed += 1
                st.session_state.history.append(st.session_state.current_word)
                st.session_state.audio_to_play = "Incorrect."
                st.session_state.last_result = ("error", f"Incorrect. The correct spelling is: {st.session_state.current_word}")
            
            st.rerun()

st.divider()

# Review list for missed words.
if st.session_state.history:
    with st.expander("Words to practice more"):
        for w in sorted(set(st.session_state.history)):
            st.write(f"• {w}")

if st.sidebar.button("Reset all scores"):
    st.session_state.correct = 0
    st.session_state.missed = 0
    st.session_state.history = []
    st.session_state.last_result = None
    st.session_state.session_started = False
    st.session_state.current_word = random.choice(st.session_state.word_list)
    st.rerun()