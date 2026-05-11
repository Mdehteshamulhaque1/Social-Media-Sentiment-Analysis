from backend.fastapi_service.app.ml.sentiment import SentimentModel


def test_sentiment_predicts():
    m = SentimentModel()
    label, score = m.predict("I love this product. It's amazing!")
    assert label in ("positive", "negative", "neutral")
    assert isinstance(score, float)
