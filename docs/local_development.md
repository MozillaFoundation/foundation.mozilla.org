# Local Development

This documentation is composed of three main sections:

- [How to use Docker in this project](#how-to-use)
- [Connecting Docker to your code editor](#connecting-docker-to-your-code-editor)
- [Docker 101 and how we use it with the foundation site](#docker-vocabulary-and-overview). Start here if you're new to Docker

We also have a list of common questions: [FAQ](#faq).

## How to use

To interact with the project, you can use [docker](https://docs.docker.com/engine/reference/commandline/cli/) and [docker-compose](https://docs.docker.com/compose/reference/overview/) CLIs or use shortcuts with invoke.

The general workflow is:

- Install the project with `invoke new-env`,
- Run the project with `docker-compose up`,
- Log into the admin site with username `admin` and password `admin`,
- Use invoke commands for frequent development tasks (database migrations, dependencies install, run tests, etc),
- After doing a `git pull`, keep your clone up to date by running `invoke catchup`.

### Invoke commands

To get a list of invoke commands available, run `invoke -l`:

```
  catch-up (catchup, docker-catchup)              Rebuild images, install dependencies, and apply migrations
  compilemessages (docker-compilemessages)        Compile the latest translations
  makemessages (docker-makemessages)              Extract all template messages in .po files for localization
  makemigrations (docker-makemigrations)          Creates new migration(s) for apps
  manage (docker-manage)                          Shorthand to manage.py. inv docker-manage "[COMMAND] [ARG]"
  migrate (docker-migrate)                        Updates database schema
  new-db (docker-new-db)                          Delete your database and create a new one with fake data
  copy-stage-db                                   Overwrite your local docker postgres DB with a copy of the staging database
  copy-prod-db                                    Overwrite your local docker postgres DB with a copy of the production database
  new-env (docker-new-env)                        Get a new dev environment and a new database with fake data
  npm (docker-npm)                                Shorthand to npm. inv docker-npm "[COMMAND] [ARG]"
  npm-install (docker-npm-install)                Install Node dependencies
  pip-compile (docker-pip-compile)                Shorthand to pip-tools. inv pip-compile "[filename]" "[COMMAND] [ARG]"
  pip-compile-lock (docker-pip-compile-lock)      Lock prod and dev dependencies
  pip-sync (docker-pip-sync)                      Sync your python virtualenv
  start-dev (docker-start, start)                 Start the dev server
  start-lean-dev (docker-start-lean, start-lean)  Start the dev server without rebuilding
  test (docker-test)                              Run both Node and Python tests
  test-node (docker-test-node)                    Run node tests
  test-python (docker-test-python)                Run python tests
```

Note the above commands carefully, as they should cover the majority of what you'd need for local development.

For instance, you can run also run common Django commands via invoke, such as `inv manage "makemigrations --merge"` or `inv manage shell`.

**A few examples:**

- `invoke manage load_fake_data`: add more fake data to your project,
- `invoke npm "install gsap"`: install gsap, add it to your `package.json` and lock it.

### Docker and docker-compose CLIs

We strongly recommend you to check at least the [docker-compose CLI](https://docs.docker.com/compose/reference/overview/) documentation since we're using it a lot. Meanwhile, here are the commands you will use the most:

**docker-compose:**

- [docker-compose up](https://docs.docker.com/compose/reference/up/): start the services and the project. Stop them with `^C`. If you want to rebuild your images, for example after a python dependencies update, add the `--build` flag. If you want to run the services in detached mode, use `--detached`. To get logs, use `docker-compose logs --follow [SERVICE]`,
- [docker-compose down](): stop and remove the services,
- [docker-compose run (--rm) [SERVICE NAME] [COMMAND]](https://docs.docker.com/compose/reference/run/): run a command against a service. `--rm` removes your container when you're done,
- [docker-compose build [SERVICE NAME]](https://docs.docker.com/compose/reference/build/): build a new image for the service. Use `--no-cache` to build the image from scratch again,
- [docker-compose ps](https://docs.docker.com/compose/reference/ps/): list the services running.

**docker:**

- [docker image](https://docs.docker.com/engine/reference/commandline/image/): interact with images,
- [docker container](https://docs.docker.com/engine/reference/commandline/container/): interact with containers,
- [docker volume](https://docs.docker.com/engine/reference/commandline/volume_create/): interact with volumes.
- [docker system prune](https://docs.docker.com/engine/reference/commandline/system_prune/): delete all unused container, image and network. Add `--volumes` to also remove volume. :rotating_light: It will impact other docker project running on your system! For a more subtle approach, [check this blog post](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes) on to remove elements selectively.

### How to install or update dependencies?

#### Python

**Note on [pip-tools](https://github.com/jazzband/pip-tools)**:

- Only edit the `.in` files and use `invoke pip-compile-lock` to generate `.txt` files.
- Both `(dev-)requirements.txt` and `(dev-)requirements.in` files need to be pushed to Github.
- `.txt` files act as lockfiles, where dependencies are pinned to a precise version.

Dependencies live on your filesystem: you don't need to rebuild the `backend` image when installing or updating dependencies.

**Install packages:**

- Modify the `requirements.in` or `dev-requirements.in` to add the dependency you want to install.
- Run `invoke pip-compile-lock`.
- Run `invoke pip-sync`.

**Update packages:**

- `invoke pip-compile --filename=requirements.in --command="--upgrade"`: update all dependencies in requirements.in.
- `invoke pip-compile --filename=dev-requirements.in --command="--upgrade-package [PACKAGE](==x.x.x)"`: update the specified dependency in dev-requirements.txt. To update multiple dependencies, you always need to add the `-P` flag. E.g. `invoke pip-compile --filename=dev-requirements.in --command="-P black==23.3.0 -P isort"`

When it's done, run `inv pip-sync`.

#### JS

**Install packages:**

Use `invoke npm "install [PACKAGE]"`.

**Update packages:**

Use `invoke npm update` or `invoke npm "update [PACKAGE](==x.x.x)"`.

### Using a copy of the staging database for critical testing

Requirements:

- Heroku Account with membership on the Mozilla team (ask in #mofo-engineering on Slack)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) - remember to run `heroku login` after installation finishes.

You can copy the staging database using `inv copy-stage-db`, or the production database using `inv copy-prod-db`.

**Note** that this script requires that docker is not already ready running, as this script requires exclusive database access. You can ensure that this is the case by running `docker-compose down` twice in the repo's root directory. The first time should show all running containers getting shut down, the second should confirm that there is nothing to take down anymore.

For more control, you can also manually invoke `node copy-db.js`, which has the following behavior:

```
  node copy-db.js             Copy the staging database.
  node copy-db.js --prod      Copy the production database.
```

In addition, you can add a `--keep` runtime flag when invoking the script, in which case the database dump file will not be deleted after completion.

If the copy script is invoked when the correct database dump file already exists, it will not redownload it and simply reuse the file on disk.

---

## Connecting Docker to your code editor

### Pycharm

This feature is only available for the professional version of Pycharm. Follow the official instructions [available here](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html#config-docker)

### Visual Studio Code

Visual Studio Code uses a feature called Dev Container to run Docker projects. The configuration files are in the `.devconatainer` directory. This feature is only available starting VSCode 1.35 stable. For now, we're only creating a python container to get Intellisense, we're not running the full project inside VSCode. We may revisit this in the future if Docker support in VSCode improves.

A few things to keep in mind when using that setup:

- Do not use the terminal in VSCode when running `invoke docker-` commands: use a local terminal instead,
- when running `inv docker-catchup` or installing python dependencies, you will need to rebuild the Dev Container. To do that, press `F1` and look for `Rebuild Container`.

#### Instructions:

- Install the [Remote - containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers),
- Open the project in VSCode: it detects the Dev Container files and a popup appears: click on `Reopen in a Container`,
- Wait for the Dev Container to build,
- Work as usual and use the docker invoke commands in a terminal outside VSCode.

#### Debugging

Ensure you have the official [python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for Visual Studio Code installed. It provides the debugging type required for the run configuration to work.

1. Set the `VSCODE_DEBUGGER` value to `True` in your .env

2. Rebuild your Docker containers: `inv docker-catchup`, then `docker-compose up`

3. Start the debug session from VS Code for the `[django:docker] runserver` configuration

   1. Open up the debugger, or open the Command Palette and select
      `View: Show Run and Debug`.

   2. Select `[django:docker] runserver` from the dropdown near the Play button in the top left.

   3. Hit the Play button or hit `F5` to start debugging

      - Logs will redirect to your integrated terminal as well.

4. Set some breakpoints!

   - You can create a breakpoint by clicking to the left of a line number. When that code is
     executed, the debugger will pause code execution so you can inspect the call stack and
     variables. You can either resume code execution or manage code execution manually by stepping
     into the next pieces of code, or over them.

---

## Docker vocabulary and overview

Welcome to Docker! Before jumping into Docker installation, take a moment to get familiar with Docker vocabulary:

- Docker: Docker is a platform to develop, deploy and run applications with containers.
- Docker engine: The Docker engine is a service running in the background (daemon). It's managing containers.
- Docker CLI: Command Line Interface to interact with Docker. For example, `Docker image ls` lists the images available on your system.
- Docker hub: Registry containing Docker images.
- Image: An image is a file used to build containers: In our case, it's mostly instructions to install dependencies.
- Container: Containers run an image. In our case, we have a container for the database, another one for building static files and the last one for running Django. A container life is ephemeral: data written there don't persist when you shut down a container.
- Volume: A volume is a special directory on your machine that is used to make data persistent. For example, we use it to store the database: that way, you don't lose your data when you turn down your containers.
- Host: host is used in Docker docs to mean the system on top of which containers run.
- Docker-compose: It's a tool to run multi-container applications: we use it to run our three containers together.
- Docker-compose CLI: Command line interface to interact with docker-compose. It's used to launch your dev environment.
- Docker-compose service: a service is a container and the configuration associated to it.

I would recommend watching [An Intro to Docker for Djangonauts](https://www.youtube.com/watch?v=qsEfVSTZO9Q) by Lacey Williams Henschel (25 min, [repo mentioned in the talk](https://github.com/williln/docker-hogwarts)): it's a great beginner talk to learn Docker and how to use it with Django.

### Project Structure

All our containers run on Linux.

For local development, we have use a multi stage Dockerfile to define our image:

- The `frontend` stage use a node8 Debian Stretch slim base image from the Docker Hub and install node dependencies,
- The `base` and `dev`: use a python3.9 Debian Stretch slim base image, install required build dependencies before installing pipenv and the project dependencies.
  We don't have a custom image for running postgres and use one from the Docker Hub.

The `docker-compose.yml` file describes the 2 services that the project needs to run:

- `postgres`: contains a postgres database,
- `backend`: runs Django. Starting this one automatically starts the postgres service.

Within the `backend` container, [Honcho](https://honcho.readthedocs.io/en/latest/index.html#) is used with `Procfile.dev` to run the `web` process (for the webserver), and the `frontend-watch` process to watch the frontend assets and rebuild static files when they're modified.

#### Starting dev container without rebuilding frontend

There is also a `docker-compose-lean.yml` file which starts the container with just the `backend` service without running the frontend watch process. This is to provide an option for a faster start up, as the frontend watch process can take a while to rebuild the static assets. 

Note that a side effect of this is that this could be using outdated frontend assets, e.g. stylesheets are not reflecting the latest changes, or the frontend assets can be missing if the container is new and `npm run build` has not been run to create `network-api/networkapi/frontend` yet.

To start up the dev container normally, use `inv start` or `docker-compose up`. To start it as a lean container without frontend build, use `inv start-lean` or `docker-compose -f docker-compose.yml -f docker-compose-lean.yml up`.


### Resources about Docker

- [Docker](https://docs.docker.com/) and [Docker-compose](https://docs.docker.com/compose/overview/) documentations,
- [Intro to Docker](https://www.revsys.com/tidbits/brief-intro-docker-djangonauts/): Lacey wrote a good intro tutorial to Docker and Django, without Harry Potter metaphors this time :),
- [Jérôme Petazzoni's training slides and talks](https://container.training/): presentations and slides if you want to dive into Docker.

#### Useful commands using Django with Docker

To open a terminal session inside the docker container:
`docker exec backend bash`
Activate the python environment:
`source dockerpythonvenv/bin/activate`

Then you can do Django stuff like:
`cd network-api/ && python manage.py makemigrations --merge`
or run Django shell, etc.

---

## FAQ

### Do I need to build the static files before doing a `docker-compose up`?

Static files are automatically built when starting the `backend` container, except when using `inv start-lean` (see "Starting dev container without rebuilding frontend" above). 

### Where is Docker fitting in all the tools we're already using?

Let's do a quick overview of all the tools you're currently using to run the foundation site on your computer:

- `npm`: use to manage javascript dependencies (`packages.json`, `packages-lock.json`). Also used to launch commands like `npm run start`.
- `pip-tools`: use to manage python dependencies (`(dev-)requirements.in` and `(dev-)requirements.txt`).
- `invoke`/`inv`: use as a cli tool to provide shortcuts for most used commands. ex: `inv migrate` is a shortcut for `docker-compose run --rm backend ./dockerpythonvenv/bin/python network-api/manage.py migrate`.

We still use all those tools with Docker. The major difference is that `npm` and `python` are now running inside a container, while invoke continues to run outside of it.

### Can I use Docker in parallel with the old way of running the foundation site?

Short answer is yes, but those two environments won't share their dependencies: you will have to maintain and update both of them.
