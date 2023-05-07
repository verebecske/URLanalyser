FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt requirements.txt
EXPOSE 5000

RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "app.py"]

