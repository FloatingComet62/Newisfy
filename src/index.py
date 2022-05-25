from flask import Flask, render_template, request, jsonify
from news import get_news

app = Flask(__name__)

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