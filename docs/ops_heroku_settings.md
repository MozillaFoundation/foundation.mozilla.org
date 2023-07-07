# OPS and Heroku Settings

## Staging

"Automatic deployment" feature on Heroku is enabled for the staging environment. Changes merged into the `main` branch will get automatically deployed to staging.

The staging URLs are:

- [foundation.mofostaging.net](https://foundation.mofostaging.net) for the Foundation website
- [mozillafestival.mofostaging.net](https://mozillafestival.mofostaging.net) for the Mozilla festival website

## Production

Production deployments are done by promoting the staging app to production in the Heroku pipeline.
This is done on the Heroku dashboard.
See also: https://devcenter.heroku.com/articles/pipelines#deployment-with-pipelines

The production URLs are:

- [foundation.mozilla.org](https://foundation.mozilla.org) for the Foundation website
- [mozillafestival.org](https://www.mozillafestival.org/en/) for the Mozilla festival website

## Domain Redirect

Enable domain redirection by setting `DOMAIN_REDIRECT_MIDDLEWARE_ENABLED` to `True`. This will enable a middleware function that checks every request, and returns a 307 redirect to the first listed domain in `TARGET_DOMAINS` if the host header does not match one of the domains specified there.

## Special purposes Environment Variables

- `USE_COMMENTO`: If Commento.io commenting is to be enabled, set this to `True`. Don't forget to add the js domain to your CSP directives for script-src and child-src
