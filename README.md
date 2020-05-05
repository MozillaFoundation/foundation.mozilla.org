# foundation.mozilla.org

[![Build Status](https://travis-ci.org/mozilla/foundation.mozilla.org.svg?branch=master)](https://travis-ci.org/mozilla/foundation.mozilla.org)
[![Dependency Status](https://david-dm.org/mozilla/network.svg)](https://david-dm.org/mozilla/network)
[![Dev Dependency Status](https://david-dm.org/mozilla/network/dev-status.svg)](https://david-dm.org/mozilla/network/?type=dev)
[![Uses Mofo Standards](https://MozillaFoundation.github.io/mofo-standards/badge.svg)](https://github.com/MozillaFoundation/mofo-standards)
[![Code Coverage](https://coveralls.io/repos/github/mozilla/foundation.mozilla.org/badge.svg?branch=master)](https://coveralls.io/github/mozilla/foundation.mozilla.org)

## Table of contents

[Setup](#setup)

[Setup with Docker](#how-to-setup-your-dev-environment-with-docker)

[Local development with invoke and pipenv](docs/local_development_with_invoke_pipenv.md)

[Local development with Docker](docs/local_development_with_docker.md)

[Engineer Workflow](docs/workflow.md)

[OPS and Heroku Settings](docs/ops_heroku_settings.md)

[Scheduled Task](docs/scheduled.md)

[Stack](docs/stack.md)

## How to Setup your Dev Environment with Pipenv and Invoke

**Requirements**: [Node](https://nodejs.org), [npm](https://www.npmjs.com/), [git](https://git-scm.com/), [python3.6 or later](https://www.python.org/), [pip](https://pypi.python.org/pypi), [pipenv](https://docs.pipenv.org/), [invoke](https://www.pyinvoke.org/installing.html), [gettext](https://www.gnu.org/software/gettext/).

If you installed [Python with Homebrew](https://docs.brew.sh/Homebrew-and-Python), use `pip3 install` instead of `pip install` when installing the relevant requirements.

### Check your environment

- `python --version` should return 3.7 or higher,
- `pipenv --version` should return 11.10 or higher,
- `invoke --version` should return 0.22.1 or higher,
- `gettext --version` should return 0.20.1 or higher.

### Setup steps

Run the following terminal commands to get started:

- `git clone https://github.com/mozilla/foundation.mozilla.org.git`
- `cd foundation.mozilla.org`
- `inv setup`

If you're on windows, you need an extra step: run `inv manage createsuperuser` to create an admin user.

You're done :tada:

To catch up on new dependencies, migrations, etc. after initial setup, you can use the `inv catch-up` command.

For more information on how to run this project, check the [local development with invoke and pipenv](docs/local_development_with_invoke_pipenv.md) documentation.

## Testing

### Code tests

When relevant, we encourage you to write tests. You can run the tests using `inv docker-test`, or you can run the Node and Python testing suites separately:

- Run Node tests: `inv docker-test-node`
- Run Python tests: `inv docker-test-python`

### Visual regression tests

In addition to the code tests there are also visual regression tests, located in the `./cypress/integration` directory. You can run these tests locally by installing [cypress](https://www.cypress.io/) using `npm i cypress@3.0.3`, after which the command `npm run cypress` will run these tests locally. However, note that these tests are currently intended for screenshot comparisons across branches, and so will not yield any meaningful results when run for a single branch.

### Accessibility tests (a11y tests)

Accessibility tests are not part of the standard tests covered by `inv test`. You can run them locally by running `npm install` and `npm run cypress:install` once, after which the following command will run the a11y testing:

- `npm run cypress:a11y`

Note that when tests fail, the `./cypress/screenshots` directory will contain one screenshot for each failed test.

## How to Setup your Dev Environment with Docker

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (macOS and Windows). For Linux users: install [Docker CE](https://docs.docker.com/install/#supported-platforms) and [Docker Compose](https://docs.docker.com/compose/install/). If you don't want to create a Docker account, direct links to download can be found [in this issue](https://github.com/docker/docker.github.io/issues/6910),
- [Check your install](https://docs.docker.com/get-started/#test-docker-version) by running `docker run hello-world`,
- If relevant: delete your node_modules directory (`rm -rf node_modules`). It's not necessary, but it speeds up the install.
- Run `invoke docker-new-env` ([install invoke](http://www.pyinvoke.org/installing.html) if you don't have it yet).

This task creates a `.env` that is in charge of managing your environment variables while running Docker. The installation will take a few minutes: you need to download images from the Docker Hub, install JS and Python dependencies, create fake data, migrate your database, etc.

When it's done, run `docker-compose up`, wait until the static files to be built, and go to `0.0.0.0:8000`. You should have a local working version of the foundation site with fake data. When you want to stop, do `^C` to shut down your containers.

To log into the admin site, a superuser will have been created with username `admin` with password `admin`.

For more information on how to run the project with Docker, check the [local development with Docker](docs/local_development_with_docker.md) documentation.

## Mozilla Festival

The fake data generator can generate a site structure for the Mozilla Festival that can be served under it's own domain, or in the case of review apps on Heroku, where we're limited to a single domain, as a sub-directory of the main foundation site, at `{review_app_host}/mozilla-festival`.

In order to access the Mozilla Festival site locally on a different domain than the main Foundation site, you'll need to edit your hosts file (`/etc/hosts` on *nix systems, `C:\Windows\System32\Drivers\etc\hosts` on Windows) to allow you to access the site at `mozfest.localhost:8000`. To enable this, add the following line to your hosts file: `127.0.0.1 mozfest.localhost`

## Gotchas

As this is REST API and CMS built on top of Django, there are some "gotcha!"s to keep in mind due to the high level of magic in the Django code base (where things will happen automatically without the code explicitly telling you).

#### **DEBUG=True**

The `DEBUG` flag does all sorts of magical things, to the point where testing with debugging turned on effectively runs a completely different setup compared to testing with debugging turned off. When debugging is on, the following things happen:

- Django bypasses the `ALLOWED_HOST` restrictions, which again can lead to `400 Bad Request` errors in `DEBUG=False` setting.
- Rather than HTTP error pages, Django will generate stack traces pages that expose pretty much all environment variables except any that match certain substrings such as `KEY`, `PASS`, etc. for obvious security reasons.
- ...there are probably more gotchas just for `DEBUG` so if you find any please add them to this list.

## Translations

Translations of UI strings (from the Django and React apps) are stored in [the fomo-l10n repository](https://github.com/mozilla-l10n/fomo-l10n). Translations are happening in Pontoon, in multiple projects: [Foundation website](https://pontoon.mozilla.org/projects/mozilla-foundation/), [\*Privacy Not Included](https://pontoon.mozilla.org/projects/privacy-not-included/) and [Mozilla Festival](https://pontoon.mozilla.org/projects/mozilla-festival/).

The latest source strings are regularly exposed to Pontoon by a Localization PM using the following process:

### Initial setup:
- Clone the `fomo-l10n` repository locally.
- Set the `LOCAL_PATH_TO_L10N_REPO` variable in your `.env` file. Use the absolute path to your copy of the `fomo-l10n` repository and include the trailing slash. E.g. `LOCAL_PATH_TO_L10N_REPO=/Users/username/Documents/GitHub/fomo-l10n/`

### Exposing latest source strings:
- Make sure your local repositories of `fomo-l10n` and `foundation.mozilla.org` are matching the latest revision from master.
- Run `inv docker-makemessages` from your `foundation.mozilla.org` repository.
- Files should have been updated in your `fomo-l10n` repository. You can now create a pull-request.

### Getting the latest translations for local dev

Latest translations are uploaded to S3. To get them, run:
- `curl -o translations.tar https://foundation-site-translations.s3.amazonaws.com/translations.tar`
- `tar -C network-api -xvf translations.tar`

You don't need to run `compilemessages` and it works for both pipenv or docker workflows.

The `translations_github_commit_[...]` file from the archive is only used for debug purposes on Heroku. It can be safely deleted if needed.

## Contributing

We love contributors, but the team maintaining this project is small and not structured to significantly support new and inexperienced contributors. If there's an unassigned issue that catches your eye, feel free to open a PR for it, but keep in mind our support will be limited. We usually don't have the capacity to walk you through the process of spinning up the project, opening a PR or describing what the solution to the issue could be.
