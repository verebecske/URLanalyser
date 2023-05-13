FROM python:3.10-alpine

WORKDIR .
COPY requirements.txt requirements.txt
EXPOSE 5000
RUN pip install -r requirements.txt

RUN apk upgrade --no-cache --available \
    && apk add --no-cache \
      chromium 

RUN apk add dbus
RUN export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_PATH=/usr/lib/chromium/

COPY . .

CMD [ "python", "main.py"]

