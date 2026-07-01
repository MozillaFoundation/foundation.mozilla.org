## Environment Variables

Environment variables are loaded from a `.env` file in the project root (gitignored) for local development, and must be set in [Heroku config vars](https://devcenter.heroku.com/articles/config-vars) for staging and production. See `foundation_cms/settings/base.py` for the full list with defaults.

### Required (no defaults — the app will error on startup without these)

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `CONTENT_TYPE_NO_SNIFF` | `bool` — sets `SECURE_CONTENT_TYPE_NOSNIFF` |
| `SET_HSTS` | `bool` — enables HSTS |
| `XSS_PROTECTION` | `bool` — sets `SECURE_BROWSER_XSS_FILTER` |
| `SSL_REDIRECT` | `bool` — redirects HTTP → HTTPS |
| `X_FRAME_OPTIONS` | e.g. `DENY` or `SAMEORIGIN` |

### Core

| Variable | Default | Description |
|---|---|---|
| `DEBUG` | `False` | Enables Django debug mode. See [DEBUG=True gotchas](#debugtrue) below |
| `DATABASE_URL` | `None` | Postgres connection string, e.g. `postgresql://user@host:5432/db` |
| `ALLOWED_HOSTS` | `[]` | Comma-separated list of allowed hostnames |
| `CSRF_TRUSTED_ORIGINS` | `[]` | Trusted origins for CSRF |
| `DJANGO_SECRET_KEY` | — | Secret key for Django |
| `REDIS_URL` | `""` | Redis connection string; enables caching when set |
| `WAGTAILADMIN_BASE_URL` | `""` | Base URL for Wagtail admin email links |

### Auth (Auth0)

| Variable | Default | Description |
|---|---|---|
| `SOCIAL_AUTH_AUTH0_DOMAIN` | `None` | Auth0 domain |
| `SOCIAL_AUTH_AUTH0_KEY` | `None` | Auth0 application key |
| `SOCIAL_AUTH_AUTH0_SECRET` | `None` | Auth0 application secret |
| `SOCIAL_AUTH_LOGIN_REDIRECT_URL` | `None` | Redirect URL after login |

### Storage / CDN

| Variable | Default | Description |
|---|---|---|
| `USE_S3` | `True` | Use S3 for media storage; set `False` for local dev |
| `AWS_ACCESS_KEY_ID` | — | S3 credentials |
| `AWS_SECRET_ACCESS_KEY` | — | S3 credentials |
| `AWS_STORAGE_BUCKET_NAME` | — | S3 bucket name |
| `AWS_S3_CUSTOM_DOMAIN` | — | Custom domain for S3-served assets |
| `AWS_LOCATION` | `""` | Key prefix within the S3 bucket |
| `ASSET_DOMAIN` | `""` | Legacy asset domain |
| `STATIC_HOST` | `""` | CDN host for static files (empty in DEBUG or review apps) |
| `FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN` | `""` | Cloudflare cache purge token |
| `FRONTEND_CACHE_CLOUDFLARE_ZONEID` | `""` | Cloudflare zone ID for cache purging |

### Error Tracking / Monitoring

| Variable | Default | Description |
|---|---|---|
| `SENTRY_DSN` | `None` | Sentry DSN; Sentry is disabled when unset |
| `SENTRY_ENVIRONMENT` | `None` | Sentry environment tag |
| `SCOUT_KEY` | `""` | Scout APM key; Scout is disabled when unset |
| `SCOUT_NAME` | `"foundation"` | Scout APM app name |

### External Services

| Variable | Default | Description |
|---|---|---|
| `BASKET_URL` | `""` | Basket newsletter service URL |
| `PULSE_API_DOMAIN` | `""` | Mozilla Pulse API domain |
| `GITHUB_TOKEN` | `""` | GitHub token for review app automation |
| `SLACK_WEBHOOK_RA` | `""` | Slack webhook for review app notifications |
| `PETITION_TEST_CAMPAIGN_ID` | `""` | Salesforce campaign ID for petition testing |
| `PNI_STATS_DB_URL` | `None` | \*Privacy Not Included stats database URL |
| `CAMO_ENDPOINT_KEY` | `""` | Camo image proxy key |
| `CAMO_NEWSLETTER_ENDPOINT` | `""` | Camo newsletter endpoint |
| `NEWSLETTER_SIGNUP_METHOD` | `""` | Newsletter signup method |
| `UNSUBSCRIBE_NEWSLETTER_ENDPOINT` | `""` | Newsletter unsubscribe endpoint |
| `SUCCESSFUL_UNSUBSCRIBE_REDIRECT_URL` | `""` | Redirect after successful unsubscribe |
| `APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION` | `""` | Apple Pay domain key for Foundation |
| `APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST` | `""` | Apple Pay domain key for Mozfest |

### Wagtail Localize (Git sync)

| Variable | Default | Description |
|---|---|---|
| `WAGTAILLOCALIZE_GIT_URL` | `""` | Git repo URL for Wagtail Localize |
| `WAGTAILLOCALIZE_GIT_DEFAULT_BRANCH` | `""` | Default branch for localization repo |
| `WAGTAILLOCALIZE_GIT_CLONE_DIR` | `""` | Local clone directory |
| `WAGTAIL_LOCALIZE_PRIVATE_KEY` | `""` | SSH private key for the localization repo |

### Heroku / Review Apps

| Variable | Default | Description |
|---|---|---|
| `APP_ENVIRONMENT` | `""` | Set to `"Review"` on review apps |
| `REVIEW_APP` | `False` | `True` when running on a Heroku review app |
| `HEROKU_APP_NAME` | `""` | Heroku app name (set automatically by Heroku) |
| `HEROKU_RELEASE_VERSION` | `None` | Release version (set automatically by Heroku) |
| `HEROKU_BRANCH` | `""` | Git branch name (set automatically by Heroku) |
| `HEROKU_PR_NUMBER` | `""` | PR number (set automatically by Heroku) |
| `REVIEW_APP_HEROKU_API_KEY` | `None` | Heroku API key for review app teardown |
| `REVIEW_APP_CLOUDFLARE_ZONE_ID` | `None` | Cloudflare zone for review app DNS |
| `REVIEW_APP_CLOUDFLARE_TOKEN` | `None` | Cloudflare token for review app DNS |
| `REVIEW_APP_DOMAIN` | `None` | Review app public domain |
| `PROD_HOSTNAMES` | `""` | Production hostnames (used when copying prod DB to staging) |
| `STAGING_HOSTNAMES` | `""` | Staging hostnames |

### Development / Local Only

| Variable | Default | Description |
|---|---|---|
| `DEBUG_TOOLBAR_ENABLED` | `False` | Enable Django Debug Toolbar |
| `PATTERN_LIBRARY_ENABLED` | `False` | Enable the Wagtail pattern library |
| `FORCE_500_STACK_TRACES` | `False` | Force stack traces on 500 errors in non-DEBUG mode |
| `RANDOM_SEED` | `None` | Seed for randomized test data |
| `VSCODE_DEBUGGER` | `False` | Attach VS Code debugger via `debugpy` |
| `LOCAL_PATH_TO_L10N_REPO` | — | Absolute path to local `fomo-l10n` clone (see [Translations](#translations)) |
| `WAGTAIL_NOTIFICATION_EMAIL` | — | Email address for Wagtail admin notifications |
| `WAGTAIL_NOTIFICATION_EMAIL_PASSWORD` | — | Password for the notification email account |

### Search App

| Variable | Default | Description |
|---|---|---|
| `SEARCH_AUTOCOMPLETE_MIN_CHARS` | `5` | Minimum number of characters required to trigger search autocomplete |

---

## Frontend Workflow for the "Redesign Site"

### Development Mode

- Make sure the `DEBUG` environment variable is set to `True` so that Django and Docker serve updated compiled files correctly.
- Run `docker-compose up` from the root of the codebase (not from `./frontend`).
- Develop as usual.

### CSS

- SCSS files are located in `./foundation_cms/static/scss`.
- These are automatically compiled into `.css` files as part of the build process.

## Frontend commands

- The frontend is composed of two yarn workspaces defined in a root `package.json` file. The two workspaces are
located in `frontend/legacy` and `frontend/redesign`. Running `yarn` commands from the root will trigger
the root scripts defined in the root `package.json` and are helper scripts defined to run for all workspaces.
To run `yarn` commands from an individual workspace, you can `cd` into the workspace, or you can use workspace
syntax from the root directory (for exapmle: `yarn workspace redesign lint`)

## Check Linting Error

From the `./frontend/redesign` directory:

- Run `yarn lint` to check JavaScript and SCSS files for linting errors.

To lint separately:

- Run `yarn lint:js` to check JavaScript files for linting errors.
- Run `yarn lint:scss` to check SCSS files using Stylelint.

## Fix Linting Error

From the `./frontend/redesign` directory:

- Run `yarn fix` to automatically fix JavaScript and SCSS linting errors.

To fix them separately:

- Run `yarn fix:js` to automatically fix fixable linting issues using ESLint.
- Run `yarn fix:scss` to automatically fix SCSS linting issues.

## Check Code Formatting

We use [Prettier](https://prettier.io) to enforce consistent code formatting.

From the `./frontend/redesign` directory:

- Run `yarn check-format` to check whether JavaScript and SCSS files are correctly formatted.

To check them separately:

- Run `yarn format:js` to check whether JavaScript files are correctly formatted.
- Run `yarn format:scss` to check whether SCSS files are correctly formatted.

## Fix Code Formatting

We use [Prettier](https://prettier.io) to enforce consistent code formatting.

From the `./frontend/redesign` directory:

- Run `yarn format` to automatically format JavaScript and SCSS files.

To format them separately:

- Run `yarn format:js` to automatically format JS code
- Run `yarn format:scss` to automatically format SCSS code

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
