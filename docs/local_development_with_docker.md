# Docker for Local Dev Documentation

This documentation is composed of three main sections:
- [How to install and use Docker for local development](./local_development_with_docker.md#how-to-use)
- [Connecting Docker to your code editor](./local_development_with_docker.md#connecting-docker-to-your-code-editor)
- [Docker 101 and how we use it with the foundation site](./local_development_with_docker.md#docker-vocabulary-and-overview). Start here if you're new to Docker
- [FAQ](./local_development_with_docker.md#faq)

## How to use

To interact with the project, you can use [docker](https://docs.docker.com/engine/reference/commandline/cli/) and [docker-compose](https://docs.docker.com/compose/reference/overview/) CLIs or use shortcuts with invoke.

The general workflow is:
- Install the project with `invoke docker-new-env`,
- Run the project with `docker-compose up`,
- Log into the admin site with username `admin` and password `admin`,
- Use invoke commands for frequent development tasks (database migrations, dependencies install, run tests, etc),
- After doing a `git pull`, keep your clone up to date by running `invoke docker-catchup`.

### Invoke commands

 To get a list of invoke commands available, run `invoke -l`:

```
  docker-catch-up (docker-catchup)   Rebuild images and apply migrations
  docker-l10n-sync                   Sync localizable fields in the database
  docker-l10n-update                 Update localizable field data (copies from original unlocalized to default localized field)
  docker-makemigrations              Creates new migration(s) for apps
  docker-manage                      Shorthand to manage.py. inv docker.manage "[COMMAND] [ARG]"
  docker-migrate                     Updates database schema
  docker-new-db                      Delete your database and create a new one with fake data
  docker-new-env                     Get a new dev environment and a new database with fake data
  docker-npm                         Shorthand to npm. inv docker.npm "[COMMAND] [ARG]"
  docker-pipenv                      Shorthand to pipenv. inv docker.pipenv "[COMMAND] [ARG]"
  docker-test-node                   Run node tests
  docker-test-python                 Run python tests
```

`docker-` prefixes all Docker commands. Note the double quotes to pass multiples arguments to `docker-manage`, `docker-pipenv` and `docker-npm` commands. There's no `invoke docker-runserver` command: use `docker-compose up` instead.

**A few examples:** `invoke docker-pipenv "install requests""`: add requests to your `Pipfile` and lock it. :rotating_light: The package won't be installed: you need to [rebuild your image](./local_development_with_docker.md#python).
- `invoke docker-manage load_fake_data`: add more fake data to your project,
- `invoke docker-npm "install moment"`: install moment, add it to your `package.json` and lock it.

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

The significant difference between the two is that python dependencies are "baked" into the image, while JS dependencies are stored in a volume.

#### Python

**Install packages:**

Use `invoke docker-pipenv "install [PACKAGE]"`.

:rotating_light: Important note! :rotating_light: This **only** add the dependency to your `Pipfile` and lock-it: it doesn't install your dependency! After running this command, run `docker-compose build backend` to create a new and updated backend image to use.

**Update packages:**

To update your dependencies, do `invoke docker-pipenv update`, then build the new image with `docker-compose build backend`.

#### JS

**Install packages:**

Use `invoke docker-npm "install [PACKAGE]"`.

**Update packages:**

Use `invoke docker-npm update`.

You don't need to rebuild the `watch-static-files` image.


---

## Connecting Docker to your code editor


### Pycharm

This feature is only available for the professional version of Pycharm. Follow the official instructions [available here](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html#config-docker)

### Visual Studio Code

Visual Studio Code use a feature called Dev Container to run Docker projects. The configuration files are in the `.devconatainer` directory. This feature is only available starting VSCode 1.35 stable. For now, we're only creating a python container to get Intellisense, we're not running the full project inside VSCode. We may revisit this in the future if Docker support in VSCode improves.

A few things to keep in mind when using that setup:
- Do not use the terminal in VSCode when running `invoke docker-` commands: use a local terminal instead,
- when running `inv docker-catchup` or installing python dependencies, you will need to rebuild the Dev Container. To do that, press `F1` and look for `Rebuild Container`.

#### Instructions:

- Install the [Remote - containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers),
- Open the project in VSCode: it detects the Dev Container files and a popup appears: click on `Reopen in a Container`,
- Wait for the Dev Container to build,
- Work as usual and use the docker invoke commands in a terminal outside VSCode.

#### Debugging


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

For local development, we have two Dockerfiles that define our images:
- `Dockerfile.node`: use a node8 Debian Stretch slim base image from the Docker Hub and install node dependencies,
- `Dockerfile.python`: use a python3.7 Debian Stretch slim base image, install required build dependencies before installing pipenv and the project dependencies.
We don't have a custom image for running postgres and use one from the Docker Hub.

The `docker-compose.yml` file describes the 3 services that the project needs to run:
- `watch-static-files`: rebuilds static files when they're modified,
- `postgres`: contains a postgres database,
- `backend`: runs Django. Starting this one automatically starts the two other ones.

### Resources about Docker

- [Docker](https://docs.docker.com/) and [Docker-compose](https://docs.docker.com/compose/overview/) documentations,
- [Intro to Docker](https://www.revsys.com/tidbits/brief-intro-docker-djangonauts/): Lacey wrote a good intro tutorial to Docker and Django, without Harry Potter metaphors this time :),
- [Jérôme Petazzoni's training slides and talks](https://container.training/): presentations and slides if you want to dive into Docker.

---

## FAQ

### Do I need to build the static files before doing a `docker-compose up`?

Static files are automatically built when starting the `watch-static-files` container.

### Where is Docker fitting in all the tools we're already using?

Let's do a quick overview of all the tools you're currently using to run the foundation site on your computer:

- `npm`: use to manage javascript dependencies (`packages.json`, `packages-lock.json`). Also used to launch commands like `npm run start`.
- `pipenv`: use to manage python dependencies (`pipfile`, `pipfile.lock`). Also manage a python virtual environment, which isolates the foundation site's python packages from the rest of your system.
- `invoke`/`inv`: use as a cli tool to provide shortcuts for most used commands. ex: `inv runserver` is a shortcut for `pipenv run python network-api/manage.py runserver`.

We still use all those tools with Docker. The major difference is that `npm` and `pipenv` is now running inside a container, while invoke continues to run as before.

### Can I use Docker in parallel with the old way of running the foundation site?

Short answer is yes but:
- you will have two different databases.
- those two environment won't share their dependencies: you will have to maintain and update both of them.
