# Temel imaj doğrudan burada tanımlı.
# ARG BUILD_FROM KULLANMAYIN: Supervisor her derlemede kendi varsayılanını
# (ghcr.io/home-assistant/base = Alpine, pip yok) --build-arg ile gönderiyor ve
# ARG varsa onu ezip derlemeyi bozuyor.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DB_PATH=/data/notlar.db

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Home Assistant eklentilerinde /data zaten kalıcıdır; docker compose ile
# çalıştırıldığında da veritabanı burada tutulur.
VOLUME ["/data"]

EXPOSE 5000

CMD ["python", "app.py"]
