import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import wavio
import tempfile
import pyttsx3
from agent import agent_response  # your LLM/RAG agent

st.set_page_config(page_title="🎙️ Aditi Voice Bot", layout="wide")
st.title("🎙️ Aditi Sharma’s Voice Bot")

# --- Record voice ---
duration = st.number_input("Recording duration (seconds)", min_value=2, max_value=15, value=5)

if st.button("🎤 Speak Now"):
    st.info("Listening...")

    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    # Save to temp WAV
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wavio.write(f.name, recording, fs, sampwidth=2)
        audio_file = f.name

    # --- Transcribe speech ---
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            query = recognizer.recognize_google(audio_data, language="en-IN")
            st.success(f" Heard: {query}")
        except sr.UnknownValueError:
            st.error(" Could not understand audio")
            query = ""
        except sr.RequestError as e:
            st.error(f"Recognition error: {e}")
            query = ""

    # --- Get agent response ---
    if query:
        prompt = f"Answer this question ONLY in the persona of Aditi Sharma: {query}"
        answer = agent_response(prompt)

        st.markdown("**Aditi says:**")
        container = st.empty()
        displayed = ""

        # Initialize TTS
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)

        # --- Stream sentences ---
        sentences = answer.split(". ")
        for s in sentences:
            displayed += s.strip() + ". "
            container.write(displayed)
            engine.say(s)
            engine.runAndWait()
