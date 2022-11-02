FROM python:3.9-alpine

WORKDIR .
COPY requirements.txt requirements.txt
EXPOSE 5000
RUN pip install -r requirements.txt

RUN apk upgrade --no-cache --available \
    && apk add --no-cache \
      chromium 

ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_PATH=/usr/lib/chromium/

COPY . .
CMD [ "python", "main.py"]

