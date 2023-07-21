FROM python:3.7

ARG INSTA_USERNAME
ARG INSTA_PASSWORD

ENV INSTA_USERNAME=$INSTA_USERNAME
ENV INSTA_PASSWORD=$INSTA_PASSWORD

COPY . /app
RUN mkdir -p /app/model
WORKDIR /app
RUN pip3 install -r local_env.txt
CMD gunicorn --bind 0.0.0.0:5000 main:app