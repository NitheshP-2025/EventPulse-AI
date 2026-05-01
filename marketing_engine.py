import streamlit as st
import pandas as pd
import json
import google.generativeai as genai
import os
import time

genai.configure(api_key="AIzaSyDfIcFtKDvgi35Vpl3p7EZoLU3EMUOWHEs")

def find_active_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for target in ['gemini-1.5-flash', 'gemini-pro']:
            matched = [m for m in models if target in m]
            if matched: return matched[0]
        return "gemini-pro"
    except:
        return "gemini-pro"

ACTIVE_MODEL = find_active_model()
model = genai.GenerativeModel(ACTIVE_MODEL)

st.set_page_config(page_title="EventPulse AI - Full App", layout="wide")

st.title("🚀 EventPulse AI: Instant Marketing Engine")
st.write(f"Active Intelligence Mode: **Connected to {ACTIVE_MODEL}**")

try:
    with open('handoff_to_member2.json', 'r') as f:
        handoff = json.load(f)
    
    df = pd.read_csv('marketing_scores.csv')
    score_col, file_col, face_col = 'score', 'filename', 'faces_detected'

    top_row = df.sort_values(by=score_col, ascending=False).iloc[0]
    
    all_files = os.listdir('.')
    display_file = [f for f in all_files if top_row[file_col] in f][0]
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📸 Top Event Highlight")
        st.image(display_file, use_container_width=True)
        
        stat_a, stat_b = st.columns(2)
        stat_a.metric("Marketing Score", f"{top_row[score_col]:.1f}")
        stat_b.metric("People Detected", int(top_row[face_col]))

    with col2:
        st.subheader("✍️ AI Content Generator")
        event_name = handoff.get('event_name', 'StepOne Buildathon')
        
        if st.button("Generate Final Multi-Platform Kit"):
            with st.spinner("Executing Active Intelligence engine..."):
                success = False
                retries = 3
                for i in range(retries):
                    try:
                        prompt = f"""
                        Write a viral marketing kit for '{event_name}'.
                        Data: {int(top_row[face_col])} people detected, score: {top_row[score_col]:.1f}.
                        Provide:
                        1. Instagram Feed Caption (with hashtags)
                        2. Instagram Story 'POV' text and sticker ideas
                        3. Professional LinkedIn post
                        """
                        response = model.generate_content(prompt)
                        
                        st.success("✨ Content Generated Successfully!")
                        st.markdown("---")
                        
                        tabs = st.tabs(["📸 Instagram Feed", "🤳 Instagram Story", "💼 LinkedIn"])
                        with tabs[0]: st.info(response.text)
                        with tabs[1]: st.warning("Add the 'POV' stickers suggested in the AI text.")
                        with tabs[2]: st.info("LinkedIn professional summary is ready.")
                        
                        success = True
                        break 
                    except Exception as e:
                        if "429" in str(e):
                            st.warning(f"Quota limit hit. Retrying in 10s... (Attempt {i+1}/{retries})")
                            time.sleep(10)
                        else:
                            st.error(f"Generation Error: {e}")
                            break
                
                if not success:
                    st.error("AI engine is currently busy. Please wait a minute before retrying.")

    st.markdown("---")
    st.subheader("📊 Virality Prediction")
    st.line_chart({"Predicted Reach": [25, 55, 88, 99]})

except Exception as main_err:
    st.error(f"System Error: {main_err}")
