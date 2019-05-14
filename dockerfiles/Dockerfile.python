FROM python:3.7-alpine

# We want output
ENV PYTHONUNBUFFERED 1
# We don't want *.pyc
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

# Install dependencies for pillow and psycopg
RUN apk add --no-cache \
    build-base \
    jpeg-dev \
    zlib-dev \
    postgresql-dev \
    postgresql-client

# Install pipenv
RUN pip install pipenv

# Copy Pipfiles in the container
COPY Pipfile Pipfile.lock ./

# Install app deps
RUN pipenv install -d
