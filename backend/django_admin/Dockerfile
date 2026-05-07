FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY backend/django_admin/requirements.txt /app/backend/django_admin/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/backend/django_admin/requirements.txt

COPY backend /app/backend
COPY shared /app/shared

EXPOSE 8001

CMD ["gunicorn", "backend.django_admin.config.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "3", "--timeout", "120"]
