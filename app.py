import streamlit as st
from groq import Groq

st.set_page_config(page_title="My English Coach", page_icon="🎙️")

st.title("🎙️ Personal English Coach")
st.write("Apni audio file upload karein ya direct record karke check karein!")

# Automatically fetch API Key from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY")

uploaded_file = st.file_uploader("Record/Upload Audio File", type=["mp3", "m4a", "wav", "ogg"])

if uploaded_file:
    if not api_key:
        st.error("API Key nahi mili. Kripya Streamlit Secrets check karein.")
    else:
        client = Groq(api_key=api_key)
        
        st.info("AI Processing chal rahi hai...")
        
        clean_filename = "audio." + uploaded_file.name.split(".")[-1]
        
        # 1. Speech to Text
        transcription = client.audio.transcriptions.create(
            file=(clean_filename, uploaded_file.read()),
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
