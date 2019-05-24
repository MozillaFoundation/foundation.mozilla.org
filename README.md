# foundation.mozilla.org

[![Build Status](https://travis-ci.org/mozilla/foundation.mozilla.org.svg?branch=master)](https://travis-ci.org/mozilla/foundation.mozilla.org)
[![Build status - Appveyor](https://ci.appveyor.com/api/projects/status/ux4vu8p5kxf99nc3/branch/master?svg=true)](https://ci.appveyor.com/project/mozillafoundation/network/branch/master)
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

**Requirements**: [Node](https://nodejs.org), [npm](https://www.npmjs.com/), [git](https://git-scm.com/), [python3.6 or later](https://www.python.org/), [pip](https://pypi.python.org/pypi), [pipenv](https://docs.pipenv.org/), [invoke](https://www.pyinvoke.org/installing.html).

If you installed [Python with Homebrew](https://docs.brew.sh/Homebrew-and-Python), use `pip3 install` instead of `pip install` when installing the relevant requirements.

### Check your environment

- `python --version` should return 3.6 or higher,
- `pipenv --version` should return 11.10 or higher,
- `invoke --version` should return 0.22.1 or higher.

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

When relevant, we encourage you to write tests. You can run the tests using the following command

- `inv test`

In addition to the code tests there are also visual regression tests, located in the `./cypress/integration` directory. You can run these tests locally by installing [cypress](https://www.cypress.io/) using `npm i cypress@3.0.3`, after which the command `npm run cypress` will run these tests locally. However, note that these tests are currently intended for screenshot comparisons across branches, and so will not yield any meaningful results when run for a single branch.


## How to Setup your Dev Environment with Docker

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (macOS and Windows). For Linux users: install [Docker CE](https://docs.docker.com/install/#supported-platforms) and [Docker Compose](https://docs.docker.com/compose/install/). If you don't want to create a Docker account, direct links to download can be found [in this issue](https://github.com/docker/docker.github.io/issues/6910),
- [Check your install](https://docs.docker.com/get-started/#test-docker-version) by running `docker run hello-world`,
- If relevant: delete your node_modules directory (`rm -rf node_modules`). It's not necessary, but it speeds up the install.
- Run `invoke docker-setup` ([install invoke](http://www.pyinvoke.org/installing.html) if you don't have it yet). If you're running on Windows, you need to run `docker-compose --rm pipenv run python network-api/manage.py createsuperuser` when the setup is finished.

This task is copying your `.env` to the new `.docker.env` that is in charge of managing your environment variables while running Docker. The installation will take a few minutes: you need to download images from the Docker Hub, install JS and Python dependencies, create fake data, migrate your database, etc.

When it's done, run `docker-compose up`, wait until the static files to be built, and go to `0.0.0.0:8000`. You should have a local working version of the foundation site with fake data. When you want to stop, do `^C` to shut down your containers.

For more information on how to run the project with Docker, check the [local development with Docker](docs/local_development_with_docker.md) documentation.


## Security

[https://snyk.io](https://snyk.io) is used to test our npm and PyPi dependencies for vulnerabilities. These tests are run on Travis and Appveyor, and will cause a build to fail when a new vulnerability is detected.

### Resolving an issue

If an issue is reported by Snyk, you have several options to remedy the problem. Firstly, the build log should contain a link to the vulnerability report on snyk.io. On that page you will find links to the issue or CVE, and information about how to resolve the problem. You should start a new feature branch and pull request to resolve this issue before merging any other features.

### Unpatched vulnerabilities

In some cases, vulnerabilities have not been patched - you will need to look at the nature of the issue and then add an exception to the `.snyk` file for it. You can install the snyk cli using `npm install -g snyk` and add the exception like so: `snyk ignore --id="SNYK-PYTHON-BOTO3-40617" --expiry="2017-12-31" --reason="No fix available"` (Replace the `id` and `reason` with relevant information). The `expiry` flag is an [RFC2822](https://tools.ietf.org/html/rfc2822#page-14) formatted date string that will cause the ignore rule to expire - useful so that we can check periodically for fixes to unpatched vulnerabilities in our dependencies.

## Mozilla Festival

The fake data generator can generate a site structure for the Mozilla Festival that can be served under it's own domain, or in the case of review apps on Heroku, where we're limited to a single domain, as a sub-directory of the main foundation site, at `{review_app_host}/en/mozilla-festival`.

In order to access the Mozilla Festival site locally on a different domain than the main Foundation site, you'll need to edit your hosts file (`/etc/hosts` on *nix systems, `C:\Windows\System32\Drivers\etc\hosts` on Windows) to allow you to access the site at `mozillafestival.localhost:8000`. To enable this, add the following line to your hosts file: `127.0.0.1 mozillafestival.localhost`

## Gotchas

As this is REST API and CMS built on top of Django, there are some "gotcha!"s to keep in mind due to the high level of magic in the Django code base (where things will happen automatically without the code explicitly telling you).

#### **DEBUG=True**

The `DEBUG` flag does all sorts of magical things, to the point where testing with debugging turned on effectively runs a completely different setup compared to testing with debugging turned off. When debugging is on, the following things happen:

- Django bypasses the `ALLOWED_HOST` restrictions, which again can lead to `400 Bad Request` errors in `DEBUG=False` setting.
- Rather than HTTP error pages, Django will generate stack traces pages that expose pretty much all environment variables except any that match certain substrings such as `KEY`, `PASS`, etc. for obvious security reasons.
- ...there are probably more gotchas just for `DEBUG` so if you find any please add them to this list.
