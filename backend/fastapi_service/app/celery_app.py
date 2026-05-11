from celery import Celery
from .core.config import settings
from .ml.sentiment import SentimentModel

celery = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

model = SentimentModel()


@celery.task(name="tasks.batch_predict")
def batch_predict_task(texts, user_id=None):
    results = []
    for t in texts:
        label, score = model.predict(t)
        results.append({"text": t, "label": label, "score": score, "user_id": user_id})
    return results
