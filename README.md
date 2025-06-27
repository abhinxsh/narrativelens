# 🧠 NarrativeLens

LLM-powered media bias and framing analyzer.

## Features
- Analyze single or multiple articles
- Detect political bias, emotional tone, framing style
- Visualize results with Plotly
- Export JSON reports

1. Install requirements:
```bash
pip install -r requirements.txt

2. Create `.env` with:
GEMINI_API_KEY="your-gemini-api-key"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

3. Launch:
streamlit run app/main.py

## Demo
[https://narrativelens.streamlit.app](https://narrativelens.streamlit.app) 