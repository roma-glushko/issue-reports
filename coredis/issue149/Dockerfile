# syntax=docker/dockerfile:1.4.2

FROM python:3.9.15-alpine

ARG POETRY_VERSION=1.3.1

RUN set -ex && \
   apk add --no-cache gcc musl-dev

RUN pip install wheel "poetry==$POETRY_VERSION"

ENV PYTHONPATH="/app/:$PYTHONPATH"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-root --no-interaction --no-ansi

COPY . /app