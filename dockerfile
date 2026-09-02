FROM python:3.14-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade "pip>=26.2" "setuptools>=83" && \
    pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 10001 bot
COPY --chown=bot:bot . .
RUN mkdir -p db photos_of_clean_weights && chown -R bot:bot db photos_of_clean_weights

USER bot

CMD ["python", "app.py"]
