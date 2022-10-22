# syntax=docker/dockerfile:1

FROM python:3.9-alpine

WORKDIR /python-docker
COPY requirements.txt requirements.txt
EXPOSE 5000
RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "app.py"]

