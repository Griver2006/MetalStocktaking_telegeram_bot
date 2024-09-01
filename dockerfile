FROM python:3.7

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV BOT_TOKEN=""

EXPOSE 8000

CMD ["python", "app.py"]
