FROM python:3.10-alpine

RUN apk add --no-cache build-base \
    && pip3 install --no-cache-dir asyncpg==0.25.0 starlette gunicorn uvicorn\
    &&  apk add --no-cache git\
    && apk add --update --no-cache g++ gcc libxslt-dev
RUN apk add --no-cache openssh-client
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*

RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . /src
