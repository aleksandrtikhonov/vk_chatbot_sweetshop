FROM python:3.11.1-alpine3.17

RUN pip install poetry

WORKDIR /app
COPY . .
RUN poetry config virtualenvs.create false && poetry install