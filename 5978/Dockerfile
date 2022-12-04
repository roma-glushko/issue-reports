FROM python:3.9.15-alpine

ARG POETRY_VERSION=1.1.14

RUN set -ex && \
   apk add --no-cache gcc musl-dev

RUN pip install wheel "poetry==$POETRY_VERSION"

ENV PYTHONPATH="/app/:$PYTHONPATH"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry export --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt

#RUN poetry config virtualenvs.create false \
#  && poetry install --no-dev --no-interaction --no-ansi

COPY . /app