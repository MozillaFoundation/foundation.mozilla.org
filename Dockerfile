# (Keep the version in sync with the node install below)
FROM node:20-bookworm-slim as frontend

# Make build & post-install scripts behave as if we were in a CI environment (e.g. for logging verbosity purposes).
ARG CI=true

WORKDIR /app

# Install front-end dependencies.
# This will create a `node_modules` directory in the current directory.
COPY package.json package-lock.json tailwind.config.js esbuild.config.js contribute.json ./
COPY ./tailwind-plugins/ ./tailwind-plugins/
RUN npm ci --no-optional --no-audit --progress=false

# Compile static files from static source at ./source to ./network-api/networkapi/frontend
# This will create a `network-api/networkapi/frontend` directory.
COPY ./source/ ./source/
COPY ./network-api/networkapi/ ./network-api/networkapi/
RUN npm run build


# We use Debian images because they are considered more stable than the alpine
# ones because they use a different C compiler. Debian images also come with
# all useful packages required for image manipulation out of the box. They
# however weight a lot, approx. up to 1.5GiB per built image.
#
# Note: This stage builds the base image for production. Presently we are not
# using this on the production site, but only use it as base for the dev build.
# Pin "bullseye" as it matches Ubuntu 20.04 -- Heroku 20 stack currently used in production.
FROM python:3.11-slim-bookworm as base

# Install dependencies in a virtualenv
ENV VIRTUAL_ENV=/app/dockerpythonvenv

RUN useradd mozilla --create-home && mkdir /app $VIRTUAL_ENV && chown -R mozilla /app $VIRTUAL_ENV

WORKDIR /app

# Set default environment variables. They are used at build time and runtime.
# If you specify your own environment variables on Heroku, they will
# override the ones set here. The ones below serve as sane defaults only.
#  * PYTHONUNBUFFERED - This is useful so Python does not hold any messages
#    from being output.
#    https://docs.python.org/3.11/using/cmdline.html#envvar-PYTHONUNBUFFERED
#    https://docs.python.org/3.11/using/cmdline.html#cmdoption-u
#  * DJANGO_SETTINGS_MODULE - default settings used in the container.
#  * PORT - default port used.
#    Heroku will ignore EXPOSE and only set PORT variable. PORT variable is
#    read/used by Gunicorn.
#  * WEB_CONCURRENCY - number of workers used by Gunicorn. The variable is
#    read by Gunicorn.
#  * GUNICORN_CMD_ARGS - additional arguments to be passed to Gunicorn. This
#    variable is read by Gunicorn
ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=networkapi.settings \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    GUNICORN_CMD_ARGS="-c gunicorn-conf.py --max-requests 1200 --max-requests-jitter 50 --access-logfile - --timeout 25"

# Make $BUILD_ENV available at runtime
ARG BUILD_ENV
ENV BUILD_ENV=${BUILD_ENV}

# Port exposed by this container. Should default to the port used by your WSGI
# server (Gunicorn). Heroku will ignore this.
EXPOSE 8000

# Install operating system dependencies.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    libffi-dev \
    python3-setuptools \
    python3-wheel \
    curl \
    git \
    gettext \
    libmagickwand-dev \
    ffmpeg \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# Don't use the root user as it's an anti-pattern and Heroku does not run
# containers as root either.
# https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
USER mozilla

# Install your app's Python requirements.
RUN python -m venv $VIRTUAL_ENV
ENV PATH=$VIRTUAL_ENV/bin:$PATH
RUN pip install -U pip==23.3.2 && pip install pip-tools setuptools wheel
# Normally we won't install dev dependencies in production, but we do it here to optimise
# docker build cache for local build
COPY --chown=mozilla ./requirements.txt ./dev-requirements.txt ./
# Pre-install wheel before syncing, even though it's in dev-requirements.in
RUN pip-sync requirements.txt dev-requirements.txt

# Copy application code.
# Any change in this directory is likely to invalidate build cache for all lines below.
# Utilise .dockerignore to minimise cache invalidation.
COPY --chown=mozilla . .

# Copy compiled assets from the frontend build stage for collectstatic to work.
# This will later be obscured by the `network-api` bind mount in docker-compose.yml, and
# will need to be recreated by `npm run build`.
COPY --chown=mozilla --from=frontend /app/network-api/networkapi/frontend ./network-api/networkapi/frontend

# Run collectstatic to move static files from application directories and
# compiled static directory (network-api/networkapi/frontend) to the site's static
# directory in /app/network-api/staticfiles that will be served by the WSGI server.
#
# Note: this is only used where DEBUG=False, and so is not needed on dev builds.
# The network-api/staticfiles will not be visible after mounting the
# network-api directory.
RUN SECRET_KEY=none python ./network-api/manage.py collectstatic --noinput --clear

# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
# Note: this will be overridden by other commands below for dev builds.
CMD gunicorn networkapi.wsgi:application

# Below is used for local dev builds only
FROM base as dev

# Swap user, so the following tasks can be run as root
USER root

# Install `psql`, useful for `manage.py dbshell`, dependencies for installing nodejs
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    postgresql-client \
    ca-certificates \
    gnupg

# Install node (Keep the version in sync with the node container above)
# Download and import the Nodesource GPG key
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

# Create deb repository for Node.js v20.x
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list

# Update and install Node.js
RUN apt-get update && apt-get install nodejs -y \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# Restore user
USER mozilla

# Pull in the node modules from the frontend build stage so we don't have to run npm ci again.
# This is just a copy in the container, and is not visible to the host machine.
# We can't mount this as the empty directory in the host will obscure our the installed content.
# See https://docs.docker.com/storage/bind-mounts/#mount-into-a-non-empty-directory-on-the-container
COPY --chown=mozilla --from=frontend /app/node_modules ./node_modules

# To avoid isort `fatal: detected dubious ownership in repository at '/app'` error
RUN git config --global --add safe.directory /app

# do nothing forever - exec commands elsewhere
CMD tail -f /dev/null
