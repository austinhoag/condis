FROM python:3.7-slim-buster

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD celery worker -A celery_worker.cel --loglevel=info	