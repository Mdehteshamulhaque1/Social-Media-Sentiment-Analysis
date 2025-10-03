from flask import Flask, request, jsonify 
from textblob import TextBlob # type: ignore
import json
import os

app = Flask(__name__)

KEYWORDS_FILE = "keywords.json"

def load_keywords():
    """Load keywords from JSON file."""
    if not os.path.exists(KEYWORDS_FILE):
        return {"positive": [], "negative": []}
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_keywords(data):
    """Save keywords back to JSON file."""
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ✅ Home Route (fix for your problem)
@app.route("/")
def home():
    return "✅ Flask Sentiment API is Running! Use /analyze or /keywords routes."

@app.route("/analyze", methods=["POST"])
def analyze_text():
    """Analyze sentiment of given text."""
    text = request.json.get("text", "")
    if not text.strip():
        return jsonify({"error": "Text is required"}), 400

    # Sentiment using TextBlob
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    sentiment = "Neutral"
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"

    return jsonify({
        "text": text,
        "sentiment": sentiment,
        "polarity": polarity
    })

@app.route("/keywords", methods=["GET"])
def get_keywords():
    """Return current keywords."""
    return jsonify(load_keywords())

@app.route("/keywords/add", methods=["POST"])
def add_keyword():
    """Add new keyword to positive/negative list."""
    data = request.json
    word = data.get("word", "").strip().lower()
    category = data.get("category", "").lower()

    if not word or category not in ["positive", "negative"]:
        return jsonify({"error": "Invalid input"}), 400

    keywords = load_keywords()
    if word not in keywords[category]:
        keywords[category].append(word)
        save_keywords(keywords)

    return jsonify({"message": f"'{word}' added to {category} keywords."})

if __name__ == "__main__":
    app.run(debug=True)
