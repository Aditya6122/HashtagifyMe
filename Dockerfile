FROM python:3.7
RUN apt-get update && apt-get install -y git

RUN sudo apt-get install -y chromium-browser

ARG INSTA_USERNAME
ARG INSTA_PASSWORD

ENV INSTA_USERNAME=$INSTA_USERNAME
ENV INSTA_PASSWORD=$INSTA_PASSWORD

COPY . /app
WORKDIR /app

RUN pip3 install -r local_env.txt
RUN mkdir -p model
RUN gdown --id 1vxmwsSSUQ0MTjfQ2uSAc9J96ezuoh9aa -O /app/model/best_model.pth
RUN python model_load.py

CMD ["python", "main.py"]
# CMD gunicorn --bind 0.0.0.0:5000 main:app