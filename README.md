# foundation.mozilla.org

## Getting started

Before you start working on the project, be sure to read this README and the linked docs.

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

Once the webserver is running, you can log in to the admin site at http://localhost:8000/cms/. A superuser will have been created with username `admin` with password `admin`.

To catch up on new dependencies, migrations, etc. after initial setup, you can use the `inv catch-up` command. To get a full new environment with a new database, run `inv new-env` again.

Use `inv -l` to get a list of all the available invoke commands.

More information on how to work with Docker and how to manage Python dependencies are available in the [local development](docs/local_development.md) part of the documentation.

## Code style

To ensure a consistent code style and quality, we use linters and formatters.

### Linting

To check the code base for quality and style issues run `inv lint`.
This will run all configured linters.
You can run the linters individually with, e.g. `inv lint-js` for JavaScript only.
Check available commands with `inv -l`.

### Formatting

If `inv lint` shows linting errors you can try running `inv format` to fix style issues.
`inv format` should automatically fix most formatting issues.

There might be some linting issues that can not be fixed automatically.

## Testing

### Unit tests

When relevant, we encourage you to write tests.

You can run the tests using `inv test`.
This will the full test suite.

To run only a subset or a specific Python test, you can use following command:

```console
inv test-python --file path/to/file.py
```

The `test-python` command also support flags for turning increased verbosity on/off (`-v`) and
for running tests in parallel (the `-n` option). To run tests with 4 parallel processes and increased
verbosity, use:

```console
inv test-python -v -n 4
```

The `-n` flag also supports the `auto` value, which will run tests with as many parallel cores as possible.
For more info, consult the [pytest-xdist docs](https://pytest-xdist.readthedocs.io/en/stable/distribution.html).

See also [the Django docs on running tests](https://docs.djangoproject.com/en/4.1/topics/testing/overview/#running-tests).

There is currently no unit test framework for JavaScript tests set up.

### Integration tests

**(Note that this is still a work in progress.)**

Integration testing is done using [Playwright](https://playwright.dev/), with the integration tests found in `./tests/integration`.

You can run these tests locally by running a one-time `npm install` and `npm run playwright:install` after which you should be able to run `npm run playwright` to run the visual tests, with `docker-compose up` running in a secondary terminal.

In order to run the same tests as will run during CI testing, make sure that `RANDOM_SEED=530910203` is set in your `.env` file, and that your local database is a new db based on that seed (`inv new-db`).

#### URL checker

URL checker can be initiated by running `docker-compose up` in one terminal and running `npm run playwright:urls` in a secondary terminal. It checks to see if visiting the URLs listed in [`tests/foundation-urls.js`](https://github.com/MozillaFoundation/foundation.mozilla.org/blob/main/tests/foundation-urls.js) and [`tests/mozfest-urls.js`](https://github.com/MozillaFoundation/foundation.mozilla.org/blob/main/tests/mozfest-urls.js) returns an OK response (i.e., status 200). Note that the URL lists in these two files are not complete and will require updates. We will also need to expand the lists to include PNI and Donate URLs.

### Visual regression tests

We also use Playwright in combination with Browserstack's [Percy](https://percy.io/) to perform visual regression testing for PRs, using `./tests/visual.spec.js` as screenshot baseline.

Visual regression tests are run after a pull request review has been approved.

### Accessibility tests

Accessibility tests are currently unavailable but will use [axe-playwright](https://www.npmjs.com/package/axe-playwright) when the switchover from Cypress to Playwright is complete.

## Mozilla Festival

The fake data generator can generate a site structure for the Mozilla Festival that can be served under it's own domain, or in the case of review apps on Heroku, where we're limited to a single domain, as a sub-directory of the main foundation site, at `{review_app_host}/mozilla-festival`.

In order to access the Mozilla Festival site locally on a different domain than the main Foundation site, you'll need to edit your hosts file (`/etc/hosts` on *nix systems, `C:\Windows\System32\Drivers\etc\hosts` on Windows) to allow you to access the site at `mozfest.localhost:8000`. To enable this, add the following line to your hosts file: `127.0.0.1 mozfest.localhost`

Ticket purchases are implemented using a third-party integration with [Tito](https://ti.to/).
A `Tito Event` snippet can be created for each event for which registration is needed. A `TitoWidget` Streamfield block can be used to place a button on a page to open the Tito widget, linked to a specific `Tito Event`.
A `Tito Event` needs a security token and newsletter question ID which can be found in the Customize -> Webhooks section of the Tito admin dashboard for the event.
A webhook (Django view) receives requests from Tito when a ticket is completed in order to sign users up for the Mozilla newsletter.

## Donate Site

Similar to the Mozilla Festival site, the fake data generator can generate a site structure for the Donation site that can be served under it's own domain.

For local development, the donate site can be found at `donate.localhost:8000`.

## Gotchas

As this is REST API and CMS built on top of Django, there are some "gotcha!"s to keep in mind due to the high level of magic in the Django code base (where things will happen automatically without the code explicitly telling you).

#### **DEBUG=True**

The `DEBUG` flag does all sorts of magical things, to the point where testing with debugging turned on effectively runs a completely different setup compared to testing with debugging turned off. When debugging is on, the following things happen:

- Django bypasses the `ALLOWED_HOST` restrictions, which again can lead to `400 Bad Request` errors in `DEBUG=False` setting.
- Rather than HTTP error pages, Django will generate stack traces pages that expose pretty much all environment variables except any that match certain substrings such as `KEY`, `PASS`, etc. for obvious security reasons.
- ...there are probably more gotchas just for `DEBUG` so if you find any please add them to this list.

## Translations

Translations of UI strings (from the Django and React apps) are stored in [the fomo-l10n repository](https://github.com/mozilla-l10n/fomo-l10n). Translations are happening in Pontoon, in multiple projects: [Foundation website](https://pontoon.mozilla.org/projects/mozilla-foundation-website/), [\*Privacy Not Included](https://pontoon.mozilla.org/projects/privacy-not-included/) and [Mozilla Festival](https://pontoon.mozilla.org/projects/mozilla-festival/).

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
- `tar -C foundation_cms -xvf translations.tar`

You don't need to run `compilemessages` and it works for both pipenv or docker workflows.

The `translations_github_commit_[...]` file from the archive is only used for debug purposes on Heroku. It can be safely deleted if needed.

## Contributing

We love contributors, but the team maintaining this project is small and not structured to significantly support new and inexperienced contributors. If there's an unassigned issue that catches your eye, feel free to open a PR for it, but keep in mind our support will be limited. We usually don't have the capacity to walk you through the process of spinning up the project, opening a PR or describing what the solution to the issue could be.
