import streamlit as st
from groq import Groq

st.set_page_config(page_title="My English Coach", page_icon="🎙️")

st.title("🎙️ Personal English Coach")
st.write("Apni audio file upload karein ya direct record karke check karein!")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

uploaded_file = st.file_uploader("Record/Upload Audio File", type=["mp3", "m4a", "wav", "ogg"])

if uploaded_file and api_key:
    client = Groq(api_key=api_key)
    
    st.info("AI Processing chal rahi hai...")
    
    # 1. Speech to Text
    transcription = client.audio.transcriptions.create(
        file=(uploaded_file.name, uploaded_file.read()),
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

elif uploaded_file and not api_key:
    st.warning("Kripya sidebar mein apni Groq API Key daalein.")
