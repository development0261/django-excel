FROM python:3.8.10

ENV buffered 1

WORKDIR /app

ADD . /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app/

EXPOSE 15000:8000