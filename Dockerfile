# (Keep the version in sync with the node install below)
FROM node:18-bullseye-slim as frontend

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
# ones becase they use a different C compiler. Debian images also come with
# all useful packages required for image manipulation out of the box. They
# however weight a lot, approx. up to 1.5GiB per built image.
#
# Note: This stage builds the base image for production. Presently we are not
# using this on the production site, but only use it as base for the dev build.
FROM python:3.9.9-slim as base

# Install dependencies in a virtualenv
ENV VIRTUAL_ENV=/app/dockerpythonvenv

RUN useradd mozilla --create-home && mkdir /app $VIRTUAL_ENV && chown -R mozilla /app $VIRTUAL_ENV

WORKDIR /app

# Set default environment variables. They are used at build time and runtime.
# If you specify your own environment variables on Heroku or Dokku, they will
# override the ones set here. The ones below serve as sane defaults only.
#  * PATH - Make sure that Poetry is on the PATH, along with our venv
#  * PYTHONUNBUFFERED - This is useful so Python does not hold any messages
#    from being output.
#    https://docs.python.org/3.11/using/cmdline.html#envvar-PYTHONUNBUFFERED
#    https://docs.python.org/3.11/using/cmdline.html#cmdoption-u
#  * DJANGO_SETTINGS_MODULE - default settings used in the container.
#  * PORT - default port used. Please match with EXPOSE so it works on Dokku.
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
# server (Gunicorn). This is read by Dokku only. Heroku will ignore this.
EXPOSE 8000

# Install operating system dependencies.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# Don't use the root user as it's an anti-pattern and Heroku does not run
# containers as root either.
# https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
USER mozilla

# Install your app's Python requirements.
RUN python -m venv $VIRTUAL_ENV
RUN pip install -U pip==20.0.2 && pip install pip-tools
# Normally we won't install dev dependencies in production, but we do it here to optimise 
# docker build cache for local build
COPY --chown=mozilla ./requirements.txt ./dev-requirements.txt ./
RUN pip install -r requirements.txt -r dev-requirements.txt

# Copy application code.
# Any change in this directory is likely to invalidate build cache for all lines below.
# Utilise .dockerignore to minimise cache invalidation.
COPY --chown=mozilla . .

# Copy compiled assets from the frontend build stage for collectstatic to work.
# This will later be obscured by the `network-api` bind mount in docker-compose.yml, and 
# will need to be recreated by `npm run build`.
COPY --chown=mozilla --from=frontend /app/network-api/networkapi/frontend ./network-api/networkapi/frontend

# Collect static. This command will move static files from application
# directories and "network-api/networkapi/frontend" folder to the main static directory that
# will be served by the WSGI server.
RUN SECRET_KEY=none python ./network-api/manage.py collectstatic --noinput --clear

# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
CMD gunicorn networkapi.wsgi:application

# Below is used for local dev builds only
FROM base as dev

# Swap user, so the following tasks can be run as root
USER root

# Install node (Keep the version in sync with the node container above)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs

# Install `psql`, useful for `manage.py dbshell`
RUN apt-get install -y postgresql-client

# Restore user
USER mozilla

# Pull in the node modules from the frontend build stage so we don't have to run npm ci again.
# This is just a copy in the container, and is not visible to the host machine.
COPY --chown=mozilla --from=frontend /app/node_modules ./node_modules

# To avoid isort `fatal: detected dubious ownership in repository at '/app'` error
RUN git config --global --add safe.directory /app

# do nothing forever - exec commands elsewhere
CMD tail -f /dev/null
