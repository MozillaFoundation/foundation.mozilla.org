# foundation.mozilla.org

[![Build Status](https://travis-ci.org/mozilla/foundation.mozilla.org.svg?branch=master)](https://travis-ci.org/mozilla/foundation.mozilla.org)
[![Build status - Appveyor](https://ci.appveyor.com/api/projects/status/ux4vu8p5kxf99nc3/branch/master?svg=true)](https://ci.appveyor.com/project/mozillafoundation/network/branch/master)
[![Dependency Status](https://david-dm.org/mozilla/network.svg)](https://david-dm.org/mozilla/network)
[![Dev Dependency Status](https://david-dm.org/mozilla/network/dev-status.svg)](https://david-dm.org/mozilla/network/?type=dev)
[![Uses Mofo Standards](https://MozillaFoundation.github.io/mofo-standards/badge.svg)](https://github.com/MozillaFoundation/mofo-standards)
[![Code Coverage](https://coveralls.io/repos/github/mozilla/foundation.mozilla.org/badge.svg?branch=master)](https://coveralls.io/github/mozilla/foundation.mozilla.org)

## Development

### Setup

**Requirements**: [Node](https://nodejs.org), [npm](https://www.npmjs.com/), [git](https://git-scm.com/), [python3.6 or later](https://www.python.org/), [pip](https://pypi.python.org/pypi), [pipenv](https://docs.pipenv.org/), [invoke](http://www.pyinvoke.org/installing.html).

#### Check your environment

- `python --version` should return 3.6 or higher,
- `pipenv --version` should return 11.10 or higher,
- `invoke --version` should return 0.22.1 or higher.

#### setup steps

Run the following terminal commands to get started:

- `git clone https://github.com/mozilla/foundation.mozilla.org.git`
- `cd foundation.mozilla.org`
- `inv setup`

If you're on windows, you need an extra step. Run `inv manage createsuperuser` to create an admin user.

You're done :tada:

#### Load fake model data

By default, your dev site will use production data (read only!). Fake model data can be loaded into your dev site with the following command

- `inv manage load_fake_data`

Replace `NETWORK_SITE_URL` value by `http://localhost:8000` in your `.env` file.

#### Running the server

You can run the development server using the following command

- `inv runserver`

The site should now be accessible at `https://localhost:8000`

To log in to the admin UI, visit: http://localhost:8000/admin

#### Generating a new set of fake model data

You can empty your database and create a full new set of fake model data using the following command

- `pipenv run python network-api/manage.py load_fake_data --delete`

You can generate a specific set of fake model data by entering a seed value

- `pipenv run python network-api/manage.py --delete --seed VALUE`

If a seed is not provided, a pseudorandom one will be generated and logged to the console. You can share this value with others if you need them to generate the same set of data that you have.

##### Landing Page and Campaign links

The `load_fake_data` command will output the following URLs every time:

- `/opportunity/page/`
- `/opportunity/page-with-signup/`
- `/opportunity/page-side-nav/`
- `/opportunity/page-side-nav/sub-page/`
- `/opportunity/page-side-nav/sub-page-2/`
- `/opportunity/page-side-nav/sub-page-with-signup/`
- `/campaigns/important-issue/`
- `/campaigns/important-issue/overview`
- `/campaigns/important-issue/press`
- `/campaigns/important-issue/take-action` (Petition page)
- `/campaigns/single-petition` (Petition page)

#### Running the project for front-end development

- At the root of the project you can run: `npm start`, which will start the server as well as watch tasks for recompiling changes to Pug, JS, and Sass files.

#### Tests

When relevant, we encourage you to write tests.
You can run the tests using the following command

- `inv manage test`
- `pipenv check`

---

### Stack

#### HTML

HTML for the majority of the site is generated from [Pug](https://pugjs.org) templates.

Some templates used by Mezzanine (at the time of writing: Opportunity, Campaign, and Fellowships pages) are written as Django templates but extend blocks from a common base template (`network-api/networkapi/templates/pages/base-compiled.html`) that is generated from Pug (see `source/pug/templates/base-for-django.pug`). This allows code sharing for the overall HTML "shell" of the site between Pug and Django templates as we migrate away from Pug.

Localized strings are pulled from [Java .properties](https://en.wikipedia.org/wiki/.properties) files located in `/locales`.

#### CSS

CSS is generated from [Sass](http://sass-lang.com/). The [Mofo Bootstrap](https://github.com/mozilla/mofo-bootstrap) theme is pulled in by default.

#### React

React is used *à la carte* for isolated component instances (eg: a tab switcher) since this is not a single page application, but rather a static generated website. This precludes the need for Flux architecture, or such libraries as React Router.

To add a React component, you can target a container element from `/source/js/main.js` and inject it.

#### Django and Mezzanine

Django powers the backend of the site, and we use Mezzanine with Django to provide CMS features and functionality.

---

### File Structure

```
/
├── dest <- Compiled code generated from source. Don't edit!
├── network-api <- Django site code
│   ├── networkapi <- Django apps live within this directory
│   └── templates <- page templates and overrides
├── locales <- Localized strings (Java .properties syntax)
├── scripts <- Scripts run by npm tasks
└── source <- Source code
    ├── images <- Image assets
    ├── js <- JS code
    │   └── components <- React components
    ├── json <- JSON for static data sets
    │   └── temp <- JSON pulled from web services. Don't commit!
    ├── pug <- Pug templates
    └── sass <- Sass code
```

---

## Development

This project is based on Mezzanine, which is itself based on Django, so the documentation for both projects applies. As far as Django is concerned, there is "good documentation" on the Django site but it's primarily considered good by people who already know Django, which is kind of bad. If this is your first foray into Django, you will want to read through https://djangobook.com/ instead.

### Pipenv and Invoke commands

TODO

### Overriding templates and static content

Sometimes it is necessary to override templates or static js/css/etc assets. In order to track *what* we changed in these files please surround your changes with:

```
# override: start #123
... override code here...
# override: end #123
```

Where `#...` is an issue number pointing to the issue that these changes are being made for.

### Gotchas

As this is REST API and CMS built on top of Django, there are some "gotcha!"s to keep in mind due to the high level of magic in the Django code base (where things will happen automatically without the code explicitly telling you).

#### **DEBUG=True**

The `DEBUG` flag does all sorts of magical things, to the point where testing with debugging turned on effectively runs a completely different setup compared to testing with debugging turned off. When debugging is on, the following things happen:

- Django uses its own built-in static content server, in which template tags may behave *differently* from the Mezzanine static server, which can lead to `400 Bad Request` errors in `DEBUG=False` setting.
- Django bypasses the `ALLOWED_HOST` restrictions, which again can lead to `400 Bad Request` errors in `DEBUG=False` setting.
- Rather than HTTP error pages, Django will generate stack traces pages that expose pretty much all environment variables except any that match certain substrings such as `KEY`, `PASS`, etc. for obvious security reasons.
- ...there are probably more gotchas just for `DEBUG` so if you find any please add them to this list.

#### Use of `{ static "...." }` in templates

Using the `static` tag in templates is supposed both in Django and Mezzanine, but they work differently: in Django, `{static "/..." }` works fine, but in Mezzanine this is a breaking pattern and there **should not** be a leading slash: `{ static "..." }`.

### Deployment

#### Staging

Builds to staging are triggered by commits to `master`.

Staging URL is [foundation.mofostaging.net](https://foundation.mofostaging.net)

#### Production

Production deployments are done by promoting Staging in the Heroku pipeline.

Production URL is [foundation.mozilla.org](https://foundation.mozilla.org)

##### Domain Redirect

Enable domain redirection by setting `DOMAIN_REDIRECT_MIDDLWARE_ENABLED` to `True`. This will enable a middleware function that checks every request, and return a 307 redirect to `TARGET_DOMAIN` if the host header does not match it.

---

### Environment Variables

Default environment variables are declared in `env.default`. If you wish to override any of the values, you can create a local `.env` file in the root of the project. This file should not be committed.

The domain used to fetch static content from Network Pulse can be customized by specifying `PULSE_API_DOMAIN`. By default it uses `network-pulse-api-production.herokuapp.com`.

The URL for fetching static content from the Network API can be customized by specifying `NETWORK_SITE_URL`. By default it uses `https://foundation.mozilla.org`. **NOTE: this variable must include a protocol (such as `https://`)**

---
### Security

[https://snyk.io](https://snyk.io) is used to test our npm and PyPi dependencies for vulnerabilities. These tests are run on Travis and Appveyor, and will cause a build to fail when a new vulnerability is detected.

#### Resolving an issue

If an issue is reported by Snyk, you have several options to remedy the problem. Firstly, the build log should contain a link to the vulnerability report on snyk.io. On that page you will find links to the issue or CVE, and information about how to resolve the problem. You should start a new feature branch and pull request to resolve this issue before merging any other features.

#### Unpatched vulnerabilities

In some cases, vulnerabilities have not been patched - you will need to look at the nature of the issue and then add an exception to the `.snyk` file for it. You can install the snyk cli using `npm install -g snyk` and add the exception like so: `snyk ignore --id="SNYK-PYTHON-BOTO3-40617" --expiry="2017-12-31" --reason="No fix available"` (Replace the `id` and `reason` with relevant information). The `expiry` flag is an [RFC2822](https://tools.ietf.org/html/rfc2822#page-14) formatted date string that will cause the ignore rule to expire - useful so that we can check periodically for fixes to unpatched vulnerabilities in our dependencies.
