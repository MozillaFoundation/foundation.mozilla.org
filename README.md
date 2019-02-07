# foundation.mozilla.org

[![Build Status](https://travis-ci.org/mozilla/foundation.mozilla.org.svg?branch=master)](https://travis-ci.org/mozilla/foundation.mozilla.org)
[![Build status - Appveyor](https://ci.appveyor.com/api/projects/status/ux4vu8p5kxf99nc3/branch/master?svg=true)](https://ci.appveyor.com/project/mozillafoundation/network/branch/master)
[![Dependency Status](https://david-dm.org/mozilla/network.svg)](https://david-dm.org/mozilla/network)
[![Dev Dependency Status](https://david-dm.org/mozilla/network/dev-status.svg)](https://david-dm.org/mozilla/network/?type=dev)
[![Uses Mofo Standards](https://MozillaFoundation.github.io/mofo-standards/badge.svg)](https://github.com/MozillaFoundation/mofo-standards)
[![Code Coverage](https://coveralls.io/repos/github/mozilla/foundation.mozilla.org/badge.svg?branch=master)](https://coveralls.io/github/mozilla/foundation.mozilla.org)

## Setup

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

## Development

### Pipenv and Invoke commands

Pipenv pattern to run Django management commands is:

- `pipenv run python [path to manage.py] [manage.py command] [options]`

For example, you can run your development server that way:

- `pipenv run python network-api/manage.py runserver`

But it's a bit long. So instead, you can use invoke:

- `inv runserver`

### Invoke tasks available:

- `inv -l`: list available invoke tasks
- `inv makemigrations`: Creates new migration(s) for apps
- `inv migrate`: Updates database schema
- `inv runserver`: Start a web server
- `inv setup`: Prepare your dev environment after a fresh git clone
- `inv test`: Run tests
- `inv catch-up`: Install dependencies and apply migrations

For management commands not covered by an invoke tasks, use `inv manage [command]` (example: `inv manage load_fake_data`). You can pass flag and options to management commands using `inv manage [command] -o [positional argument] -f [optional argument]`. For example:
- `inv manage runserver -o 3000`
- `inv manage load_fake_data -f seed=VALUE`
- `inv manage migrate -o news`

### Generating a new set of fake model data

By default, your dev site will use production data (read only!). To load fake model data into your dev site:

- Run `inv manage load_fake_data`
- Replace `NETWORK_SITE_URL` value with `http://localhost:8000` in your `.env` file.

You can empty your database and create a full new set of fake model data using the following command

- `pipenv run python network-api/manage.py load_fake_data --delete`

You can generate a specific set of fake model data by entering a seed value

- `pipenv run python network-api/manage.py --delete --seed VALUE`

Alternatively, the seed value can be specified through the use of the `RANDOM_SEED` environment variable.

If a seed is not provided, a pseudorandom one will be generated and logged to the console. You can share this value with others if you need them to generate the same set of data that you have.

### Landing Page and Campaign links

The `load_fake_data` command will output pages with the following slugs:

- `/`
- `/about/`
- `/styleguide/`
- `/people/`
- `/news/`
- `/initiatives/`
- `/campaigns/single-page/`
- `/campaigns/multi-page/`
- `/opportunity/single-page/`
- `/opportunity/multi-page/`

This list is available on review apps by clicking on `DEV HELP` in the menu or going to `[review app url]/help`.


### Resolving conflicting Django migrations

**AKA: What to do when someone else's migration for the same app lands before yours**

- Create a new, separate local instance of `foundation` per "Setup steps" above.
- Check out your new PR branch locally.
- Delete *all* your PR's migrations and commit the deletion.
- Run `inv makemigrations`
- Commit the newly generated migration.
- Run `inv migrate` to verify and run new migration.
- Push changes to your PR branch.

### Running the project with live front-end reloading

- At the root of the project you can run `npm start`, which will start the server as well as watch tasks for recompiling changes to JS(X) and Sass files.

## Testing

When relevant, we encourage you to write tests. You can run the tests using the following command

- `inv test`

In addition to the code tests there are also visual regression tests, located in the `./cypress/integration` directory. You can run these tests locally by installing [cypress](https://www.cypress.io/) using `npm i cypress@3.0.3`, after which the command `npm run cypress` will run these tests locally. However, note that these tests are currently intended for screenshot comparisons across branches, and so will not yield any meaningful results when run for a single branch.









## Security

[https://snyk.io](https://snyk.io) is used to test our npm and PyPi dependencies for vulnerabilities. These tests are run on Travis and Appveyor, and will cause a build to fail when a new vulnerability is detected.

### Resolving an issue

If an issue is reported by Snyk, you have several options to remedy the problem. Firstly, the build log should contain a link to the vulnerability report on snyk.io. On that page you will find links to the issue or CVE, and information about how to resolve the problem. You should start a new feature branch and pull request to resolve this issue before merging any other features.

### Unpatched vulnerabilities
In some cases, vulnerabilities have not been patched - you will need to look at the nature of the issue and then add an exception to the `.snyk` file for it. You can install the snyk cli using `npm install -g snyk` and add the exception like so: `snyk ignore --id="SNYK-PYTHON-BOTO3-40617" --expiry="2017-12-31" --reason="No fix available"` (Replace the `id` and `reason` with relevant information). The `expiry` flag is an [RFC2822](https://tools.ietf.org/html/rfc2822#page-14) formatted date string that will cause the ignore rule to expire - useful so that we can check periodically for fixes to unpatched vulnerabilities in our dependencies.

## Gotchas

As this is REST API and CMS built on top of Django, there are some "gotcha!"s to keep in mind due to the high level of magic in the Django code base (where things will happen automatically without the code explicitly telling you).

#### **DEBUG=True**

The `DEBUG` flag does all sorts of magical things, to the point where testing with debugging turned on effectively runs a completely different setup compared to testing with debugging turned off. When debugging is on, the following things happen:

- Django uses its own built-in static content server, in which template tags may behave *differently* from the Mezzanine static server, which can lead to `400 Bad Request` errors in `DEBUG=False` setting.
- Django bypasses the `ALLOWED_HOST` restrictions, which again can lead to `400 Bad Request` errors in `DEBUG=False` setting.
- Rather than HTTP error pages, Django will generate stack traces pages that expose pretty much all environment variables except any that match certain substrings such as `KEY`, `PASS`, etc. for obvious security reasons.
- ...there are probably more gotchas just for `DEBUG` so if you find any please add them to this list.

#### Use of `{ static "...." }` in templates

Using the `static` tag in templates is supposed both in Django and Mezzanine, but they work differently: in Django, `{static "/..." }` works fine, but in Mezzanine this is a breaking pattern and there **should not** be a leading slash: `{ static "..." }`.


## Other important documentations 
[Development](docs/development.md)

[Critical Testing](docs/critical_testing.md)

[Deployment](docs/deployment.md)

[Scheduled Task](docs/scheduled_task.md)

[Technology Stack](docs/stack.md)