FROM python:3.11.6-alpine3.18
LABEL maintainer="imtence@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR src/
RUN pip install -r requirements.txt

COPY .src/ .
