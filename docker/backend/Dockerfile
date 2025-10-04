FROM python:3.11-slim

WORKDIR /app

COPY docker/backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app/ .

EXPOSE 8000

CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0"]
