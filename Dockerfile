FROM python:3.11.6-alpine3.18
LABEL maintainer="imtence@gmail.com"

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache gcc libc-dev musl-dev

WORKDIR /app/requirements

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .
