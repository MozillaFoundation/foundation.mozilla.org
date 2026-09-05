# Environment Variables

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
| `DEBUG` | `False` | Enables Django debug mode. See [DEBUG=True gotchas](../README.md#debugtrue) in the root README |
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
| `COOKIE_CONTROL_API_KEY` | `""` | Civic Cookie Control API key; read at JS-build time in `frontend/redesign/esbuild.config.js`, not in `settings/base.py`; banner is disabled when unset |

### Wagtail Localize (Git sync)

| Variable | Default | Description |
|---|---|---|
| `WAGTAILLOCALIZE_GIT_URL` | `""` | Git repo URL for Wagtail Localize |
| `WAGTAILLOCALIZE_GIT_DEFAULT_BRANCH` | `""` | Default branch for localization repo |
| `WAGTAILLOCALIZE_GIT_CLONE_DIR` | `""` | Local clone directory |
| `WAGTAIL_LOCALIZE_PRIVATE_KEY` | `""` | SSH private key for the localization repo |

### Wagtail Editor

| Variable | Default | Description |
|---|---|---|
| `WAGTAIL_AUTOSAVE_INTERVAL` | `0` | The autosave interval in milliseconds |

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
| `LOCAL_PATH_TO_L10N_REPO` | — | Absolute path to local `fomo-l10n` clone (see [Translations](../README.md#translations) in the root README) |
| `WAGTAIL_NOTIFICATION_EMAIL` | — | Email address for Wagtail admin notifications |
| `WAGTAIL_NOTIFICATION_EMAIL_PASSWORD` | — | Password for the notification email account |

### Search App

| Variable | Default | Description |
|---|---|---|
| `SEARCH_AUTOCOMPLETE_MIN_CHARS` | `5` | Minimum number of characters required to trigger search autocomplete |
