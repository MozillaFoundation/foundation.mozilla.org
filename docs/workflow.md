# Engineering Workflow

## Django Migrations: what to do when working on backward-incompatible migrations

### Context

[Preboot](https://devcenter.heroku.com/articles/preboot) is a feature from Heroku that prevents downtime when deploying: Heroku still serves traffic to old dynos while creating new dynos at the same time. For up to 3 minutes, two versions of the code are running and talking to the same DB: backward-incompatible changes to the DB result in internal server errors from the old code.

Most migrations are backward-compatible and don't require any special treatments. Although, if you plan to remove a field/model or rename or change a field type, you need to separate your changes in multiple PRs.

### How to prepare and deploy your backward-incompatible migrations

You can open a main issue to serve as an entry point for those PRs or link each PR to an existing issue: your choice!

Those tricky deploys require extra attention and team awareness: **they should always be scheduled in advance**. When you're ready to deploy, always announce in it `#mofo-engineering` and wait for at least a second approval.

#### Rename or change a field type

**Open three different PRs:**
- PR #1: Add the new field and its migration file (migrate data from the previous field if necessary),
- PR #2: Replace all the references of the old field by the new field
- PR #3: Remove the old field and generate the migration file

Deploy each PR separately and in ascending order.

#### Remove a field or a model

**Two different PRs:**

- PR #1: Remove all usages of the element(s) you want to remove in models, template, views, tests, etc.
- PR #2: Generate the migration

Deploy each PR separately and in ascending order.

## Continuous Integration and Review Apps

Opening a PR activates different services:
- [Review app](#review-apps): temporary apps with fake data running on Heroku,
- [Continuous Integration testing](#continuous-integration-testing): Github Actions,
- [Visual regression testing](#visual-regression-testing): Percy.

### Review Apps

#### Review App for PRs

Opening a PR will automatically create a Review App in the `foundation-site` pipeline. A slack bot posts credentials and links to Review Apps in to the `mofo-ra-foundation` Slack channel.

*Note:* This only work for Mo-Fo staff: you will need to manually open a Review App on Heroku for PRs opened by external contributors.

#### Review App for branches

You can manually create a review app for any branch pushed to this repo. It's useful if you want to test your code on Heroku without opening a PR yet.

To create one:
- log into Heroku.
- Go to the `foundation-site` pipeline.
- Click on `+ New app` and select the branch you want to use.

The review app slack bot will post a message in the `foundation-site` with links and credentials as soon as the review app is ready.

#### Environment variables:

- `REVIEW_APP`: set to True on review app.
- `GITHUB_TOKEN`: GITHUB API authentication,
- `SLACK_WEBHOOK_RA`: Webhook to `mofo-ra-foundation`

Non-secret envs can be added to the `app.json` file. Secrets must be set on Heroku in the `Review Apps` (pipelines' `settings` tab).

### Continuous Integration testing

Opening a PR will trigger [Github Action](https://github.com/mozilla/foundation.mozilla.org/actions) continuous integration, which should pass before a PR is deemed good to merge.

#### Mergify

Mergify is a bot that automatically merges PRs under certain conditions defined in `.mergify.yml`. If you want your PR to be automatically merged, add the `ready-to-merge` label to your PR. Once it's reviewed and the tests are green, Mergify takes care of rebasing to the latest `main` and merges it for you.

### Visual regression testing

The continuous integration run will also trigger a visual regression testing using [Percy.io](https://percy.io) (based on Cypress output). These tests do not need to pass for a PR to be merged in, but any discrepancies that are flagged by Percy should be reviewed and signed off on during the course of normal PR review.

Note that any changes to model fields, field ordering, or factories, will likely result in charges to our testing data, which will result in Percy flagging changes: the test data is based on Python's pseudo-random number generator, which we seed at various points during test data generation, but between those seed points is based on the exact order in which fields are assigned testing data. If the order of assignments changes, or old fields are added/new fields are removed, then the PRNG sequence will be different, and Percy will likely show that there are visual diffs that require sign-off.

It is possible that a PR has Percy-flagged changes, despite the PR not touching model/factory code nor introducing changes to the front-end code. In this case, please alert the engineering team: we've seen this happen in the past and it is unclear why it happens.
