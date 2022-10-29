FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt requirements.txt
EXPOSE 5000

RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev

RUN pip install --no-cache-dir pandas
# RUN pip install --upgrade cython
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "app.py"]

