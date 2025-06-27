import streamlit as st
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from prompts import get_bias_prompt
from utils import parse_llm_response
from visualize import bias_gauge, emotion_bar


# Load .env if you have environment variables there
load_dotenv()

# Configure Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(page_title="NarrativeLens", page_icon="🧠")
st.title("🧠 NarrativeLens: Media Bias Analyzer")
st.subheader("Clear. Concise. Unbiased.")

input_mode = st.radio("Choose input mode:", ["Single Article", "Multiple Articles"])

if input_mode == "Single Article":
    user_input = st.text_area("Paste a news article or tweet thread below:")
else:
    user_input = st.text_area("Paste multiple articles separated by --- (3 dashes):")

all_results = []

if st.button("Analyze") and user_input:
    with st.spinner("Initiating semantic breakdown..."):
        # Prepare list of articles
        if input_mode == "Single Article":
            articles = [user_input]
        else:
            articles = [a.strip() for a in user_input.split("---") if a.strip()]

        

        for idx, art in enumerate(articles):
            st.markdown(f"### 🌎🚨 Article {idx+1}")

            from google.api_core.exceptions import ResourceExhausted

            prompt = get_bias_prompt(art)
            try:
                response = model.generate_content(prompt)
                raw_result = response.text
            except ResourceExhausted:
                st.error("🚫 Daily request quota for Gemini API has been exceeded. Try again in a few hours.")
                st.stop()


            st.subheader("🔬 Bias Telemetry")
            st.code(raw_result, language="json")

            parsed = parse_llm_response(raw_result)

            if "error" in parsed:
                st.error(parsed["details"])
            else:
                st.markdown(f"**Political Bias:** {parsed['bias']}")
                st.markdown(f"**Emotional Tone:** {parsed['emotion']}")
                st.markdown(f"**Framing Style:** {parsed['framing']}")
                st.markdown("**Omitted Perspectives:**")
                st.write(parsed["omissions"])

                st.plotly_chart(bias_gauge(parsed['bias']), key=f"bias_{idx}")
                st.plotly_chart(emotion_bar(parsed['emotion']), key=f"emotion_{idx}")


            all_results.append(parsed)

if all_results:
    st.download_button(
        label="Download Results as JSON",
        data=json.dumps(all_results, indent=2),
        file_name="narrative_lens_results.json",
        mime="application/json"
    )
