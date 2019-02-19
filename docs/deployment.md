## Deployment

### Review Apps

Opening a PR will automatically create a Review App in the `foundation-site` pipeline. It's not possible to use OAuth but you can still access the admin with `admin` as the username. Login are published in the `mofo-review-apps` Slack channel when the review app is ready.

### Continuous Integration testing

Opening a PR will trigger [Travis](https://travis-ci.org) and [Appveyor](https://www.appveyor.com/) continuous integration runs, which should both pass before a PR is deemed good to merge.

### Visual regression testing

The Travis continuous integration run will also trigger a visual regression testing using [Percy.io](https://percy.io) (based on Cypress output). These tests do not need to pass for a PR to be merged in, but any discrepencies that are flagged by Percy should be reviewed and signed off on during the course of normal PR review.

### Staging

Builds to staging are triggered by commits to `master`.

Staging URL is [foundation.mofostaging.net](https://foundation.mofostaging.net)

### Production

Production deployments are done by promoting Staging in the Heroku pipeline.

Production URL is [foundation.mozilla.org](https://foundation.mozilla.org)

### Domain Redirect

Enable domain redirection by setting `DOMAIN_REDIRECT_MIDDLWARE_ENABLED` to `True`. This will enable a middleware function that checks every request, and return a 307 redirect to `TARGET_DOMAIN` if the host header does not match it.

### Environment Variables

Default environment variables are declared in `env.default`. If you wish to override any of the values, you can create a local `.env` file in the root of the project. This file should not be committed.

The domain used to fetch static content from Network Pulse can be customized by specifying `PULSE_API_DOMAIN`. By default it uses `network-pulse-api-production.herokuapp.com`.

The URL for fetching static content from the Network API can be customized by specifying `NETWORK_SITE_URL`. By default it uses `https://foundation.mozilla.org`. **NOTE: this variable must include a protocol (such as `https://`)**

#### Special purposes Environment Variables

- `GITHUB_TOKEN`: GITHUB API authentication,
- `SLACK_WEBHOOK_RA`: Webhook to `mofo-review-apps`
- `CORAL_TALK_SERVER_URL`: If Coral Talk commenting is to be enabled, set the server URL here. Don't forget to add the domain to your CSP directives for script-src and child-src


### Cloudinary for Review Apps and Staging (BuyersGuide only)

We use Cloudinary upload-mapping feature to copy images from the production to the staging Cloudinary account.

Current directories available on Cloudinary staging:

Folder | URL prefix
--- | ---
`foundationsite/buyersguide` | `https://res.cloudinary.com/mozilla-foundation/image/upload/foundationsite/buyersguide/`

To add more folders, follow [Cloudinary's instructions](https://cloudinary.com/documentation/fetch_remote_images#auto_upload_remote_resources).
