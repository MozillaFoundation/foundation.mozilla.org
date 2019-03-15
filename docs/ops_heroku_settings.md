# OPS and Heroku Settings

## Staging

Builds to staging are triggered by commits to `master`.

The staging URL is [foundation.mofostaging.net](https://foundation.mofostaging.net)

## Production

Production deployments are done by promoting Staging in the Heroku pipeline.

The production URL is [foundation.mozilla.org](https://foundation.mozilla.org)

## Domain Redirect

Enable domain redirection by setting `DOMAIN_REDIRECT_MIDDLEWARE_ENABLED` to `True`. This will enable a middleware function that checks every request, and return a 307 redirect to the first listed domain in `TARGET_DOMAINS` if the host header does not match one of the domains specified there.

## Special purposes Environment Variables

- `GITHUB_TOKEN`: GITHUB API authentication,
- `SLACK_WEBHOOK_RA`: Webhook to `mofo-review-apps`
- `CORAL_TALK_SERVER_URL`: If Coral Talk commenting is to be enabled, set the server URL here. Don't forget to add the domain to your CSP directives for script-src and child-src


## Cloudinary for Review Apps and Staging (BuyersGuide only)

We use Cloudinary upload-mapping feature to copy images from the production to the staging Cloudinary account.

Current directories available on Cloudinary staging:

Folder | URL prefix
--- | ---
`foundationsite/buyersguide` | `https://res.cloudinary.com/mozilla-foundation/image/upload/foundationsite/buyersguide/`

To add more folders, follow [Cloudinary's instructions](https://cloudinary.com/documentation/fetch_remote_images#auto_upload_remote_resources).
