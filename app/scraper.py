import requests
import os

def fetch_articles_newsapi(query, max_articles=5):
    api_key = os.getenv("NEWSAPI_KEY")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&language=en&pageSize={max_articles}&sortBy=publishedAt&apiKey={api_key}"
    )
    response = requests.get(url)
    data = response.json()

    if "articles" not in data:
        return {"error": data.get("message", "Unknown error from NewsAPI.")}

    articles = []
    for item in data["articles"]:
        articles.append({
            "title": item["title"],
            "summary": item["description"],
            "link": item["url"],
            "published": item["publishedAt"]
        })
    return articles
