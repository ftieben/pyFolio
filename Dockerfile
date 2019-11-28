FROM python:3.7-alpine
LABEL MAINTAINER Florian Tieben

RUN apk --update add \
 libc-dev \
 musl-dev \
 libffi-dev \
 openssl-dev \
 linux-headers \
 gcc \
 && rm -rf /var/cache/apk/*

RUN pip install influxdb pandas yfinance

COPY pyFolio .
COPY config .

CMD ["python3", "pyFolio/main.py"]