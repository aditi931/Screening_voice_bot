"""
Streamlit app with voice support
"""

import streamlit as st
import streamlit.components.v1 as components
from agent import agent_response

st.set_page_config(page_title="Voice RAG Bot", layout="wide")
st.title("🎙️ Aditi Sharma’s Voice Bot")

# Voice input JS
voice_js = """
<script>
const startBtn = () => {
  window.recognizedText = '';
  const status = document.getElementById('status');
  const output = document.getElementById('output');
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)){
    status.innerText = 'Speech recognition not supported in this browser.';
    return;
  }
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.lang = 'en-IN';   // ✅ Indian English for recognition
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  status.innerText = 'Listening...';
  recognition.start();
  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    output.value = text;
    const el = document.querySelector('textarea[data-testid="stTextArea"]');
    if (el) { el.value = text; el.dispatchEvent(new Event('input', { bubbles: true })); }
    status.innerText = 'Heard: ' + text;
  };
  recognition.onerror = (e) => { status.innerText = 'Error: ' + e.error; }
  recognition.onspeechend = () => { recognition.stop(); }
}

function speak(text){
  if (!('speechSynthesis' in window)) { return; }
  const msg = new SpeechSynthesisUtterance(text);
  msg.lang = 'en-IN';   //  Indian English accent
  msg.pitch = 1;        // Normal pitch
  msg.rate = 1;         // Normal speed

  // Try to pick an Indian Female voice
  const voices = window.speechSynthesis.getVoices();
  const indianFemale = voices.find(v => 
    v.lang.includes('en-IN') && v.name.toLowerCase().includes('female')
  );

  if (indianFemale) {
    msg.voice = indianFemale;
  } else {
    // fallback to any en-IN voice if female-specific not found
    const indianVoice = voices.find(v => v.lang.includes('en-IN'));
    if (indianVoice) msg.voice = indianVoice;
  }

  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(msg);
}
</script>

<div>
  <button onclick="startBtn()">Start Listening</button>
  <span id="status" style="margin-left:12px;color:gray">Not listening</span>
</div>
<textarea id="output" style="display:none"></textarea>
"""
components.html(voice_js, height=100)

query = st.text_area("Ask your question:")
if st.button("Ask"):
    if query.strip():
        answer = agent_response(query)
        st.markdown("**Answer:**")

        # Stream answer sentence by sentence
        sentences = answer.split(". ")
        container = st.empty()
        displayed = ""

        for s in sentences:
            displayed += s.strip() + ". "
            container.write(displayed)

            # Speak sentence immediately
            components.html(f"""
            <script>
              var msg = new SpeechSynthesisUtterance({s!r});
              msg.lang = 'en-US';
              window.speechSynthesis.speak(msg);
            </script>
            """, height=0)
