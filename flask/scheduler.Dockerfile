FROM python:3.7-slim-buster

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD celery beat -A celery_worker.cel --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid