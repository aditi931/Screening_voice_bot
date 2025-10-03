
import streamlit as st
import streamlit.components.v1 as components
from agent import agent_response  # Your LLM or RAG function

st.set_page_config(page_title="Aditi Voice Bot", layout="wide")
st.title("🎙️ Aditi Sharma’s Voice Bot (Fully Voice Controlled)")

# --- JS for voice recognition + auto submission + TTS ---
voice_js = """
<script>
async function startConversation() {
    const status = document.getElementById('status');

    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        status.innerText = 'Speech recognition not supported in this browser.';
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    const speak = (text) => {
        if (!('speechSynthesis' in window)) return;
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'en-IN';
        msg.pitch = 1;
        msg.rate = 1;
        const voices = window.speechSynthesis.getVoices();
        const indianFemale = voices.find(v => v.lang.includes('en-IN') && v.name.toLowerCase().includes('female'));
        if (indianFemale) msg.voice = indianFemale;
        else {
            const indianVoice = voices.find(v => v.lang.includes('en-IN'));
            if (indianVoice) msg.voice = indianVoice;
        }
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    };

    const conversation = async () => {
        status.innerText = 'Listening...';
        recognition.start();

        recognition.onresult = async (event) => {
            const text = event.results[0][0].transcript;
            status.innerText = 'Heard: ' + text;

            // Send text to Streamlit via textarea (auto submit)
            const textarea = document.querySelector('textarea[data-testid="stTextArea"]');
            if (textarea) {
                textarea.value = text;
                textarea.dispatchEvent(new Event('input', { bubbles: true }));
            }

            // Trigger Streamlit rerun
            const submitBtn = document.querySelector('button[kind="primary"]');
            if (submitBtn) submitBtn.click();
        };

        recognition.onerror = (e) => { status.innerText = 'Error: ' + e.error; }
        recognition.onspeechend = () => { recognition.stop(); }
    };

    conversation();
}
</script>

<div>
  <button onclick="startConversation()">🎤 Start Conversation</button>
  <span id="status" style="margin-left:12px;color:gray">Not listening</span>
</div>
<textarea id="voice_input" style="display:none"></textarea>
"""

components.html(voice_js, height=150)

# --- Hidden text area to receive JS input ---
query = st.text_area("Voice input (auto submitted)", key="voice_input")

# --- Process the query automatically ---
if query.strip():
    # Force all answers to Aditi persona
    prompt = f"Answer this question ONLY in the persona of Aditi Sharma: {query}"
    answer = agent_response(prompt)

    st.markdown("**Aditi says:**")
    container = st.empty()
    displayed = ""

    # Display and speak sentence by sentence
    sentences = answer.split(". ")
    for s in sentences:
        displayed += s.strip() + ". "
        container.write(displayed)

        # Speak each sentence
        components.html(f"""
        <script>
            const msg = new SpeechSynthesisUtterance({s!r});
            msg.lang = 'en-IN';
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
        </script>
        """, height=0)

    # Clear the query for next input
    st.session_state["voice_input"] = ""
