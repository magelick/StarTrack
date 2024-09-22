# pull official base image
FROM python:3.12-alpine3.19

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install Poetry
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    openssl-dev
RUN pip install -U poetry
# configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false
# Install project dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry install --only main --no-interaction --no-ansi

# copy all other fise in wotk direactory
COPY . /app/

# open by that port
EXPOSE 8000
