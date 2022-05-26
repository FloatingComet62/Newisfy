from flask import Flask, render_template, request, jsonify
import bs4
import requests
import random

app = Flask(__name__)

topics = ["all", "national", "business", "sports", "world", "politics", "technology", "startup",
    "entertainment", "miscellaneous", "hatke", "science", "automobile",]

def get_news_from_topic(topic, limit=10):
    if topic not in topics:
        return []
    topic = topic if topic != "all" else ""
    url = f"https://www.inshorts.com/en/read/{topic}"
    soup = bs4.BeautifulSoup(requests.get(url).text, "lxml")
    cards = soup.find_all("div", class_="news-card")
    news = []
    for card in cards:
        title = card.find(class_='news-card-title')
        title = title.find('a').text.strip() if title else ""

        image = card.find(class_='news-card-image')
        image = image['style'].split("'")[1] if image else ""

        summary = card.find(class_='news-card-content')
        summary = summary.find('div').text if summary else ""

        author = card.find(class_='author')
        author = author.text if author else ""

        date = card.find(clas='date')
        date = date.text if date else ""

        time = card.find(class_='time')
        time = time.text if time else ""

        link = card.find(class_='read-more')
        link = link.find('a').get('href') if link else ""

        news.append({
            'title': title,
            'image': image,
            'content': summary,
            'author': author,
            'date': f"{date}, {time}",
            'link': link
        })
    return random.sample(news, min(limit, len(news)))


def get_news(preferences:list):
    news = []
    for topic in preferences:
        if topic not in topics:
            continue
        news += get_news_from_topic(topic, limit=5)
    return news

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_news")
def get_news_route():
    try:
        preferences = request.get_json()["preferences"]
        return jsonify(get_news(preferences))
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)