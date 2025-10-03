import streamlit as st # type: ignore
import requests # type: ignore
import json
import os

# Backend API URL (agar Flask alag server pe deploy hai)
API_URL = "http://127.0.0.1:5000"

KEYWORDS_FILE = "keywords.json"

def load_keywords():
    """Load keywords from local file."""
    if not os.path.exists(KEYWORDS_FILE):
        return {"positive": [], "negative": []}
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_keywords(data):
    """Save keywords to local file."""
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Streamlit App
st.set_page_config(page_title="Social Media Sentiment Analysis", layout="wide")

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📝 Manage Keywords", "ℹ️ About"])

# ---------------- Home Page ---------------- #
if page == "🏠 Home":
    st.title("🔎 Social Media Sentiment Analysis")
    st.write("Analyze sentiment of text posts, tweets, or comments.")

    user_input = st.text_area("Enter text to analyze:", height=150)

    if st.button("Analyze Sentiment"):
        if user_input.strip():
            try:
                # Call Flask API
                response = requests.post(f"{API_URL}/analyze", json={"text": user_input})
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"**Sentiment:** {result['sentiment']}")
                    st.info(f"**Polarity Score:** {result['polarity']:.2f}")
                else:
                    st.error("Error: Could not analyze text.")
            except Exception as e:
                st.error(f"Backend not running: {e}")
        else:
            st.warning("Please enter some text.")

# ---------------- Manage Keywords Page ---------------- #
elif page == "📝 Manage Keywords":
    st.title("📝 Manage Sentiment Keywords")

    keywords = load_keywords()

    st.subheader("📖 Current Keywords")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Positive Keywords")
        st.write(", ".join(keywords["positive"]) if keywords["positive"] else "None")

    with col2:
        st.write("### Negative Keywords")
        st.write(", ".join(keywords["negative"]) if keywords["negative"] else "None")

    st.subheader("➕ Add New Keyword")
    new_word = st.text_input("Enter a keyword")
    category = st.r
