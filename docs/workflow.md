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
- [Continuous Integration testing](#continuous-integration-testing): Travis,
- [Visual regression testing](#visual-regression-testing): Percy.

### Review Apps

Opening a PR will automatically create a Review App in the `foundation-site` pipeline. It's not possible to use OAuth but you can still access the admin with `admin` as the username. Login are published in the `mofo-review-apps` Slack channel when the review app is ready.

### Continuous Integration testing

Opening a PR will trigger [Travis](https://travis-ci.org) continuous integration, which should pass before a PR is deemed good to merge.

It's possible to skip CI builds by adding `[skip ci]` or `[ci skip]` in the commit message title. If you only want to skip Travis, use `[skip travis]` or `[travis skip]`. Note: since Travis is a required check on GitHub, your last commit needs to run the CI.

### Visual regression testing

The Travis continuous integration run will also trigger a visual regression testing using [Percy.io](https://percy.io) (based on Cypress output). These tests do not need to pass for a PR to be merged in, but any discrepancies that are flagged by Percy should be reviewed and signed off on during the course of normal PR review.
