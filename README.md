# foundation.mozilla.org

[![Dependency Status](https://david-dm.org/mozilla/network.svg)](https://david-dm.org/mozilla/network)
[![Dev Dependency Status](https://david-dm.org/mozilla/network/dev-status.svg)](https://david-dm.org/mozilla/network/?type=dev)
[![Uses Mofo Standards](https://MozillaFoundation.github.io/mofo-standards/badge.svg)](https://github.com/MozillaFoundation/mofo-standards)
[![Code Coverage](https://coveralls.io/repos/github/mozilla/foundation.mozilla.org/badge.svg?branch=main)](https://coveralls.io/github/mozilla/foundation.mozilla.org)

## Table of contents

[Setup](#setup)

[Setup with Docker](#how-to-setup-your-dev-environment-with-docker)

[Local development](docs/local_development.md)

[Engineer Workflow](docs/workflow.md)

[OPS and Heroku Settings](docs/ops_heroku_settings.md)

[Scheduled Task](docs/scheduled.md)

[Stack](docs/stack.md)

## How to Setup your Dev Environment with Docker

**Requirements**: Docker ([Docker Desktop](https://www.docker.com/products/docker-desktop) for macOS and Windows or [Docker Compose](https://docs.docker.com/compose/install/) for Linux), [Python 3](https://www.python.org/downloads/) with the [invoke](https://www.pyinvoke.org/installing.html) package installed globally, and [git](https://git-scm.com/).

### Installing Invoke

We recommend that you install Invoke using [pipx](https://pypi.org/project/pipx/), but any Python package manager should work (pip, poetry, etc).

### Check your environment

- `docker run hello-world`.
- `invoke --version` should return 0.22.1 or higher.

### Setup steps

Run the following terminal commands to get started:

- `git clone https://github.com/mozilla/foundation.mozilla.org.git`
- `cd foundation.mozilla.org`
- `inv new-env`

You're done :tada:

This task creates a `.env` that is in charge of managing your environment variables while running Docker. The installation will take a few minutes: you need to download images from the Docker Hub, install JS and Python dependencies, create fake data, migrate your database, etc.

When it's done, run `docker-compose up`, wait until the static files to be built, and go to `0.0.0.0:8000`. You should have a local working version of the foundation site with fake data. When you want to stop, do `^C` to shut down your containers.

To log into the admin site, a superuser will have been created with username `admin` with password `admin`.

To catch up on new dependencies, migrations, etc. after initial setup, you can use the `inv catch-up` command. To get a full new environment with a new database, run `inv new-env` again.

Use `inv -l` to get a list of all the available invoke commands.

More information on how to work with Docker and how to manage Python dependencies are available in the [local development](docs/local_development.md) part of the documentation.

## Testing

### Code tests

When relevant, we encourage you to write tests. You can run the tests using `inv test`, or you can run the Node and Python testing suites separately:

- Run Node tests: `inv test-node`
- Run Python tests: `inv test-python`

#### Fixing linting errors

If `inv test-node` shows linting errors for either JS/JSX or CSS/SCSS, you can run the `inv npm "run fix"` command to make the linting utilities automatically fix (or at least try to fix) any errors they knows how to fix. This will almost always be the only step required to ensure the linting phase of testing passes.

### Integration tests

Integration testing is done using [Playwright](https://playwright.dev/), with the integration tests found in `./tests/integration`.

You can run these tests locally by running a one-time `npm install` and `npm run playwright:install` after which you should be able to run `npm run playwright` to run the visual tests, with `docker-compose up` running in a secondary terminal.

In order to run the same tests as will run during CI testing, make sure that `RANDOM_SEED=530910203` is set in your `.env` file, and that your local database is a new db based on that seed (`inv new-db`).

Note that this is still a work in progress.

### Visual regression tests

We also use Playwright in combination with Browserstack's [Percy](https://percy.io/) to perform visual regression testing for PRs, using `./tests/visual.spec.js` as screenshot baseline.

### Accessibility tests

Accessibility tests are currently unavailable but will use [axe-playwright](https://www.npmjs.com/package/axe-playwright) when the switchover from Cypress to Playwright is complete.

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
- Clone the [`fomo-l10n`](https://github.com/mozilla-l10n/fomo-l10n) repository locally.
- Set the `LOCAL_PATH_TO_L10N_REPO` variable in your `.env` file. Use the absolute path to your copy of the `fomo-l10n` repository and include the trailing slash. E.g. `LOCAL_PATH_TO_L10N_REPO=/Users/username/Documents/GitHub/fomo-l10n/`

### Exposing latest source strings:
- Make sure your local repositories of `fomo-l10n` and `foundation.mozilla.org` are matching the latest revision from main.
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
