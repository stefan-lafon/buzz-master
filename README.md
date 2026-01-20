# Buzz master

Buzz master is a focused spelling bee trainer designed to help students master their word lists through a "Listen, Type, Verify" loop. It uses Text-to-Speech to read words aloud and provides instant auditory and visual feedback.

## Features
* **Text-to-Speech:** Uses Google TTS to pronounce words clearly.
* **Instant Feedback:** Voice and color-coded alerts for correct and incorrect spellings.
* **Review List:** Automatically tracks missed words for end-of-session review.
* **Session Stats:** Real-time tracking of correct vs. missed attempts.
## How to use

### 1. Web app (Recommended for Chromebooks/Mobile)
Simply go to the live site:
[https://buzz-master.streamlit.app](https://buzz-master.streamlit.app)

### 2. Running locally
If you prefer to run it on your own machine using VSCode:

1. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install streamlit gTTS

2. **Prepare your words:**
   Create a words.txt file in the project folder and add your spelling words, one per line.

3. **Launch the app:**
   Run the following command in your terminal:
   ```bash
   python -m streamlit run buzz_master.py