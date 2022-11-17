# OPS and Heroku Settings

## Staging

We are deploying the `main` branch automatically to the staging environment via a [custom GitHub Actions workflow](https://github.com/mozilla/foundation.mozilla.org/blob/50ae3b68b00fcedda17d5f67d1fdfb6bca1a0f05/.github/workflows/continuous-deployment.yaml).
The "continuous deployment" workflow is triggered by the "continuous integration" workflow finishing and checks that the "continuous integration" workflow was successful.

We are using a custom action instead of the Heroku-GitHub integration because of security concerns after the [Heroku-GitHub incident in April 2022](https://status.heroku.com/incidents/2413).

The deployment workflow uses the standard Heroku git push deployment.
To run this workflow, we need to configure two secret variables for GitHub Action in https://github.com/mozilla/foundation.mozilla.org/settings/secrets/actions:

 * `HEROKU_DEPLOYMENT_USER_LOGIN` - Email address of the Heroku user to use for the push,
 * `HEROKU_DEPLOYMENT_USER_API_TOKEN` - API token of the same Heroku user. Note: API tokens are separate from API keys in Heroku. To create a new API token visit: https://dashboard.heroku.com/account/applications

The above login credentials are used to build a `.netrc` file, which is used by Git (through cURL) when pushing to Heroku.
See the [Heroku authentication docs](https://devcenter.heroku.com/articles/authentication) for more information.

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
