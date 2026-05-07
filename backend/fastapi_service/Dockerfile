FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY backend/fastapi_service/requirements.txt /app/backend/fastapi_service/requirements.txt
COPY backend /app/backend
COPY shared /app/shared
COPY app.py /app/

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/backend/fastapi_service/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.fastapi_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
