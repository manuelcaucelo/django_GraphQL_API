FROM python:3.8-slim-buster

ARG app_name="api_ideas"
ENV APP_NAME $app_name

ARG pipenv_dev=0
ENV PIPENV_DEV $pipenv_dev
ARG pipenv_cache_dir=/tmp/.pipenv_cachedir
ENV PIPENV_CACHE_DIR $pipenv_cache_dir
ENV PIPENV_MAX_SUBPROCESS=2
ENV PIPENV_MAX_DEPTH=1

ARG DOCKERIZE_VERSION="v0.6.1"

ENV PYTHONUNBUFFERED 1

ENV PIPENV_PIPFILE /tmp/Pipfile

RUN apt-get update && apt-get install -y wget libmariadb-dev-compat libcurl4-openssl-dev libssl-dev build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz && \
    mkdir -p $PIPENV_CACHE_DIR && \
    pip install pipenv

USER 1000

COPY --chown=1000 ./Pipfile $PIPENV_PIPFILE

ENV WORKON_HOME /tmp

RUN pipenv install --dev --skip-lock

COPY --chown=1000 ./api_ideas /code
