import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import io

st.set_page_config(page_title="My English Coach", page_icon="🎙️")

st.title("🎙️ Personal English Coach")
st.write("Live bol kar record karein ya pehle se bani audio file upload karein!")

# Automatically fetch API Key from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("API Key nahi mili. Kripya Streamlit Secrets check karein.")
    st.stop()

client = Groq(api_key=api_key)

# Tabs for Live Record & File Upload
tab1, tab2 = st.tabs(["🎙️ Live Record Karein", "📁 File Upload Karein"])

audio_data = None
filename = "audio.mp3"

with tab1:
    st.write("Neeche microphone button par tap karke bolna shuru karein:")
    audio_record = mic_recorder(
        start_prompt="🔴 Recording Shuru Karein",
        stop_prompt="⏹️ Recording Rokein",
        key='recorder'
    )
    if audio_record:
        audio_bytes = audio_record['bytes']
        audio_data = io.BytesIO(audio_bytes)
        filename = "live_audio.mp3"
        st.audio(audio_bytes, format='audio/mp3')

with tab2:
    uploaded_file = st.file_uploader("Audio File Select Karein", type=["mp3", "m4a", "wav", "ogg"])
    if uploaded_file:
        audio_data = uploaded_file
        filename = "uploaded_audio." + uploaded_file.name.split(".")[-1]

# Process Audio if available
if audio_data is not None:
    st.info("AI Processing chal rahi hai...")
    
    try:
        # 1. Speech to Text
        transcription = client.audio.transcriptions.create(
            file=(filename, audio_data.read()),
            model="whisper-large-v3",
            language="hi"
        )
        
        spoken_text = transcription.text
        st.success(f"**Aapne Bola:** {spoken_text}")
        
        # 2. Grammar & Vocab Fix
        prompt = f"""
        User said this Hinglish/English sentence: "{spoken_text}"
        
        Please provide:
        1. Corrected English Version
        2. Explanation of mistakes made
        3. 2 Better/Advanced Vocabulary words they could use.
        
        Keep it clear, structured, and short in easy Hinglish format.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        
        st.markdown("### 💡 AI Feedback & Correction")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Processing error: {e}")
