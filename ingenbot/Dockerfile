FROM python:3.9-alpine

WORKDIR .
COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "main.py"]
