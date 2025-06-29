import streamlit as st
import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from clustering import embed_articles, reduce_dimensions
import plotly.express as px
from prompts import get_bias_prompt, get_reframe_prompt
from utils import parse_llm_response
from visualize import bias_gauge, emotion_bar
from export import create_pdf_report


# Load environment variables
load_dotenv()

# Configure Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(page_title="NarrativeLens", page_icon="🧠")
st.title("🧠 NarrativeLens: Media Bias Analyzer")
st.subheader("Clear. Concise. Unbiased.")

with st.expander("💡 Why This Matters"):
    st.write(
        """
        Understanding bias, emotional framing, and omissions in media is essential for critical thinking and informed decision-making.
        NarrativeLens helps uncover these hidden narratives, promoting transparency and more balanced perspectives.
        """
    )

# 🎚️ Tone weight customization
EMOTIONS = {
    "neutral": 1.0,
    "joy": 1.0,
    "sadness": 1.0,
    "anger": 1.0,
    "fear": 1.0,
    "hope": 1.0,
    "disgust": 1.0,
    "surprise": 1.0
}

st.sidebar.header("🎚️ Tone Weight Customization")
emotion_weights = {}
for emotion in EMOTIONS:
    emotion_weights[emotion] = st.sidebar.slider(
        f"{emotion.capitalize()} Weight",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1
    )
st.sidebar.markdown("---")
st.sidebar.header("🕒 Analysis History")

if os.path.exists("analysis_history.json"):
    with open("analysis_history.json", "r") as f:
        history = json.load(f)

    if history:
        for idx, entry in enumerate(history[-5:][::-1]):  # show last 5
            st.sidebar.markdown(f"**{idx+1}. {entry.get('bias','Unknown').capitalize()} Bias**")
            snippet = entry.get("omissions","").strip()
            st.sidebar.caption(snippet[:60] + "...")
    else:
        st.sidebar.caption("No analyses yet.")
else:
    st.sidebar.caption("No analyses yet.")

# Bias score mapping
BIAS_SCORES = {
    "left": -1,
    "center": 0,
    "right": 1
}

# Input mode
input_mode = st.radio("Choose input mode:", ["Single Article", "Multiple Articles"])

# Manual input
if input_mode == "Single Article":
    user_input = st.text_area("Paste a news article or tweet thread below:")
else:
    user_input = st.text_area("Paste multiple articles separated by --- (3 dashes):")

# NewsAPI search
st.markdown("Or fetch recent news articles:")

search_query = st.text_input("Search for news (e.g., climate change, elections):")
fetch_articles_button = st.button("Fetch Articles")

# NewsAPI fetch logic
if fetch_articles_button and search_query:
    api_key = os.getenv("NEWSAPI_KEY")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={search_query}&language=en&pageSize=5&sortBy=publishedAt&apiKey={api_key}"
    )
    with st.spinner("Fetching articles..."):
        response = requests.get(url)
        data = response.json()

    if "articles" not in data:
        st.error(f"Error fetching articles: {data.get('message', 'Unknown error.')}")
    else:
        st.session_state.fetched_articles = [
            {
                "title": a["title"],
                "summary": a["description"],
                "link": a["url"],
                "published": a["publishedAt"]
            }
            for a in data["articles"]
        ]

# Display fetched articles for selection
selected_articles = []
if "fetched_articles" in st.session_state:
    st.markdown("### 📰 Fetched Articles:")
    for i, art in enumerate(st.session_state.fetched_articles):
        with st.expander(f"{art['title']} ({art['published']})"):
            st.write(art["summary"])
            st.markdown(f"[🌐 Read Full Article]({art['link']})")
            if st.checkbox("✅ Select this article", key=f"article_{i}"):
                selected_articles.append(art["summary"])


all_results = []

# Analyze button
if st.button("Analyze"):
    articles = []

    if "fetched_articles" in st.session_state and selected_articles:
        articles = selected_articles
    elif user_input:
        if input_mode == "Single Article":
            articles = [user_input]
        else:
            articles = [a.strip() for a in user_input.split("---") if a.strip()]

    if not articles:
        st.warning("Please input or select at least one article to analyze.")
        st.stop()

    with st.spinner("Initiating semantic breakdown..."):
        for idx, art in enumerate(articles):
            st.markdown(f"### 🌎🚨 Article {idx+1}")

            prompt = get_bias_prompt(art)
            try:
                response = model.generate_content(prompt)
                raw_result = response.text
            except Exception as e:
                if "429" in str(e) and "quota" in str(e).lower():
                    st.error(
                        "🚫 You have exceeded your Gemini API quota for today.\n\n"
                        "👉 Please wait until your daily limit resets or enable billing to continue.\n\n"
                        "[Learn more about Gemini quotas](https://ai.google.dev/gemini-api/docs/rate-limits)"
                    )
                else:
                    st.error(f"🚫 An unexpected error occurred: {str(e)}")
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
                st.markdown(f"**Predicted Source:** {parsed.get('source', 'Unknown')}")
                st.markdown("**Omitted Perspectives:**")
                st.write(parsed["omissions"])

                st.plotly_chart(bias_gauge(parsed['bias']), key=f"bias_{idx}")
                st.plotly_chart(emotion_bar(parsed['emotion']), key=f"emotion_{idx}")

                # 🎚️ Weighted tone display
                emotion_labels = [e.strip() for e in parsed['emotion'].split(",")]
                weighted_scores = {e: emotion_weights.get(e, 1.0) for e in emotion_labels}

                st.markdown("**Weighted Tone Emphasis:**")
                for e, w in weighted_scores.items():
                    st.write(f"- {e.capitalize()}: Weight x{w}")

                if st.button(f"Reframe Article {idx+1} Neutrally"):
                    reframe_prompt = get_reframe_prompt(art)
                    try:
                        reframe_response = model.generate_content(reframe_prompt)
                        reframe_text = reframe_response.text
                    except Exception as e:
                        if "429" in str(e) and "quota" in str(e).lower():
                            st.error(
                                "🚫 You have exceeded your Gemini API quota for today.\n\n"
                                "👉 Please wait until your daily limit resets or enable billing to continue.\n\n"
                                "[Learn more about Gemini quotas](https://ai.google.dev/gemini-api/docs/rate-limits)"
                            )
                        else:
                            st.error(f"🚫 An unexpected error occurred: {str(e)}")
                        st.stop()


                    st.markdown("**Neutral Rephrasing:**")
                    st.write(reframe_text)

            # Attach date info
            if "fetched_articles" in st.session_state and selected_articles:
                published_date = st.session_state.fetched_articles[idx]["published"]
            else:
                published_date = None
            parsed["published"] = published_date

            all_results.append(parsed)

    # Append to history.json
    if all_results:
        try:
            with open("analysis_history.json", "r") as f:
                existing = json.load(f)
        except FileNotFoundError:
            existing = []

        existing.extend(all_results)

        with open("analysis_history.json", "w") as f:
            json.dump(existing, f, indent=2)
        

    # Clustering
    if len(articles) >= 3:
        st.markdown("## 🧭 Semantic Similarity Map")
        with st.spinner("Generating embeddings and dimensionality reduction..."):
            clean_articles = [a.strip() for a in articles if a and len(a.strip()) > 5]

            if len(clean_articles) < 3:
                st.warning("Need at least 3 valid articles with text to generate clustering.")
            else:
                embeddings = embed_articles(clean_articles)

                if embeddings is None or embeddings.shape[0] < 3:
                    st.warning("Not enough valid embeddings to generate clustering.")
                    st.stop()
                else:
                    embedding_2d = reduce_dimensions(embeddings)
                    fig = px.scatter(
                        x=embedding_2d[:, 0],
                        y=embedding_2d[:, 1],
                        text=[a[:60] + "..." for a in clean_articles],
                        labels={"x": "Topic Similarity (X)", "y": "Topic Similarity (Y)"},
                        title="Semantic Clustering of Articles",
                        width=800,
                        height=500
                    )
                    fig.update_traces(
                        marker=dict(size=12, color="LightSkyBlue", line=dict(width=2, color="DarkSlateGrey")),
                        hovertemplate="<b>%{text}</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>"
                    )
                    st.plotly_chart(fig, key="semantic_clustering")

    # Bias over time chart
    bias_data = []
    for res in all_results:
        if res.get("published") and res.get("bias"):
            score = BIAS_SCORES.get(res["bias"].lower())
            if score is not None:
                bias_data.append({
                    "date": res["published"],
                    "bias_score": score,
                    "bias_label": res["bias"].capitalize(),
                    "snippet": res.get("omissions", "")[:80] + "..."
                })

    if bias_data:
        st.markdown("## 📈 Bias Over Time")
        df = (
            pd.DataFrame(bias_data)
            .sort_values("date")
            .reset_index(drop=True)
        )

        fig = px.scatter(
            df,
            x="date",
            y="bias_score",
            color="bias_label",
            color_discrete_map={
                "Left": "red",
                "Center": "gray",
                "Right": "blue"
            },
            hover_data={
                "bias_label": True,
                "snippet": True,
                "date": True,
                "bias_score": False
            },
            title="Political Bias Over Time",
            labels={"bias_score": "Bias (Left/Center/Right)"}
        )

        fig.update_yaxes(
            tickvals=[-1, 0, 1],
            ticktext=["Left", "Center", "Right"]
        )

        fig.update_traces(mode="lines+markers")

        st.plotly_chart(fig, key="bias_over_time")

# Download results
if all_results:
    st.download_button(
        label="🧪 Download Results as JSON",
        data=json.dumps(all_results, indent=2),
        file_name="narrative_lens_results.json",
        mime="application/json"
    )

if all_results:
    if st.button("📄 Download PDF Report"):
        create_pdf_report(all_results)
        with open("narrative_lens_report.pdf", "rb") as f:
            st.download_button(
                label="Download NarrativeLens_Report.pdf",
                data=f,
                file_name="narrative_lens_report.pdf",
                mime="application/pdf"
            )