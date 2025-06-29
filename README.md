# 🧠 NarrativeLens

A cutting-edge media analysis tool that uses large language models to detect and visualize political bias, emotional tone, and framing styles in news articles and social media content.

---

## ✨ Features

✅ Analyze single or multiple articles  
✅ Detect:
- Political bias
- Emotional tone
- Framing style
- Omitted perspectives

✅ Visualize results with interactive Plotly charts  
✅ Customize tone weighting  
✅ Generate semantic clustering of articles  
✅ Track bias over time  
✅ Export JSON and PDF reports

---

## ⚙️ Installation

1️⃣ **Clone this repository:**

```bash
git clone https://github.com/abhinxsh/narrativelens.git
cd narrativelens
````

2️⃣ **Install dependencies:**

```bash
pip install -r requirements.txt
```

3️⃣ **Create a `.env` file in the project root and add your Gemini API key:**

```
GEMINI_API_KEY="your-gemini-api-key"
NEWSAPI_KEY="your-newsapi-key"
```

✅ **Note:**
You don’t need to manually call `genai.configure()`—it’s already handled in the code.

---

## 🚀 Usage

Launch the app locally:

```bash
streamlit run app/main.py
```

---

## 🌐 Demo

Try the live demo here:
[https://narrativelens.streamlit.app](https://narrativelens.streamlit.app)

---

## 📝 Example Workflow

* Paste or fetch articles
* Click **Analyze**
* Explore:

  * Bias telemetry
  * Emotional tone
  * Framing style
  * Omitted perspectives
* Generate neutral rephrasings
* View:

  * Semantic similarity maps
  * Bias trends over time
* Download structured reports

---

## 📄 License

MIT License. Feel free to use and adapt.

---

## 🤝 Contributing

Pull requests are welcome! If you find issues or have ideas, open an issue or PR.