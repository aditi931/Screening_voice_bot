import streamlit as st
import streamlit.components.v1 as components
from agent import agent_response

st.set_page_config(page_title="Aditi Voice Bot", layout="wide")
st.title("🎙️ Aditi Sharma’s Voice Bot ")

# --- JS for voice recognition + auto submit + TTS ---
voice_js = """
<script>
async function startConversation() {
    const status = document.getElementById('status');
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window')) {
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
        const voices = window.speechSynthesis.getVoices();
        const indianFemale = voices.find(v => v.lang.includes('en-IN') && v.name.toLowerCase().includes('female'));
        if (indianFemale) msg.voice = indianFemale;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    };

    recognition.onresult = async (event) => {
        const text = event.results[0][0].transcript;
        status.innerText = 'Heard: ' + text;

        // Use Streamlit events: find the hidden input by id
        const hidden_input = document.getElementById('voice_input_hidden');
        hidden_input.value = text;

        // Dispatch input event to trigger Streamlit rerun
        hidden_input.dispatchEvent(new Event('input', { bubbles: true }));
    };

    recognition.onerror = (e) => { status.innerText = 'Error: ' + e.error; }
    recognition.onspeechend = () => { recognition.stop(); }

    status.innerText = 'Listening...';
    recognition.start();
}
</script>

<div>
  <button onclick="startConversation()">🎤 Start Conversation</button>
  <span id="status" style="margin-left:12px;color:gray">Not listening</span>
</div>
"""

components.html(voice_js, height=150)

# --- Hidden input Streamlit will detect ---
query = st.text_input("", key="voice_input_hidden", label_visibility="collapsed")

# --- Auto process query ---
if query.strip():
    prompt = f"Answer this question ONLY in the persona of Aditi Sharma: {query}"
    answer = agent_response(prompt)

    st.markdown("**Aditi says:**")
    container = st.empty()
    displayed = ""

    for s in answer.split(". "):
        displayed += s.strip() + ". "
        container.write(displayed)
        components.html(f"""
        <script>
            const msg = new SpeechSynthesisUtterance({s!r});
            msg.lang = 'en-IN';
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
        </script>
        """, height=0)

    # Clear input for next round
    st.session_state["voice_input_hidden"] = ""
