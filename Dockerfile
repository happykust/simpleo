FROM python:3.10-alpine

WORKDIR /backend

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry && poetry config virtualenvs.create false

COPY . /backend

RUN poetry install --no-interaction

ENV PYTHONPATH=/backend
