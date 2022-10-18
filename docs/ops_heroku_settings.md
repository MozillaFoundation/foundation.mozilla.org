# OPS and Heroku Settings

## Staging

~~Builds to staging are triggered by commits to `main`.~~

Automatic deployments are currently broken.
To get your work deployed after the PR has been merged to `main`, check that the [GitHub Actions CI running on `main`](https://github.com/mozilla/foundation.mozilla.org/actions?query=branch%3Amain) is passing.

Once CI has passed you can pull the branch to local and push it to Heroku.

```console
git switch main
git fetch origin
git pull origin main
git push heroku-staging main
```

For the above to work you will need access to the app on Heroku as well as the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed.
Set up the Heroku git remote as `heroku-staging`, following the docs (except for the remote name): https://devcenter.heroku.com/articles/git


The staging URLs are:

- [foundation.mofostaging.net](https://foundation.mofostaging.net) for the Foundation website
- [mozillafestival.mofostaging.net](https://mozillafestival.mofostaging.net) for the Mozilla festival website

## Production

Production deployments are done by promoting Staging in the Heroku pipeline.

The production URLs are:

- [foundation.mozilla.org](https://foundation.mozilla.org) for the Foundation website
- [mozillafestival.org](https://www.mozillafestival.org/en/) for the Mozilla festival website

## Domain Redirect

Enable domain redirection by setting `DOMAIN_REDIRECT_MIDDLEWARE_ENABLED` to `True`. This will enable a middleware function that checks every request, and returns a 307 redirect to the first listed domain in `TARGET_DOMAINS` if the host header does not match one of the domains specified there.

## Special purposes Environment Variables

- `USE_COMMENTO`: If Commento.io commenting is to be enabled, set this to `True`. Don't forget to add the js domain to your CSP directives for script-src and child-src
