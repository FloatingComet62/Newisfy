import bs4
import requests
import random

topics = [
    "all",
    "national",
    "business",
    "sports",
    "world",
    "politics",
    "technology",
    "startup",
    "entertainment",
    "miscellaneous",
    "hatke",
    "science",
    "automobile",
]

def get_news_from_topic(topic, limit=10):
    if topic not in topics:
        return []
    topic = topic if topic != "all" else ""
    url = f"https://www.inshorts.com/en/read/{topic}"
    soup = bs4.BeautifulSoup(requests.get(url).text, "lxml")
    cards = soup.find_all("div", class_="news-card")
    news = []
    for card in cards:
        news.append({
            "title": card.find("div", class_="news-card-title").find('a').text.strip(),
            'author': card.find(class_='author').text,
            "on": card.find(clas='date').text + ", " + card.find(class_='time').text,
            "summary": card.find(class_='news-card-content').find('div').text,
            "image": card.find(class_='news-card-image')['style'].split("'")[1],
            "link": card.find(class_='read-more').find('a').get('href'),
        })
    return random.sample(news, min(limit, len(news)))


def get_news(preferences:list):
    news = []
    for topic in preferences:
        if topic not in topics:
            continue
        news += get_news_from_topic(topic, limit=5)
    return news