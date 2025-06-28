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

- [Review app](#review-apps): temporary apps with fake data running on Heroku (*this is currently not working*),
- [Continuous integration testing](#continuous-integration-testing): Github Actions,
- [Visual regression testing](#visual-regression-testing): Percy.

### Review Apps

**REVIEW APPS ARE CURRENTLY NOT WORKING**

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

#### Environment variables

- `REVIEW_APP`: Set to `True` on review app.
- `GITHUB_TOKEN`: GITHUB API authentication,
- `SLACK_WEBHOOK_RA`: Webhook to `mofo-ra-foundation`
- `DEBUG_TOOLBAR_ENABLED`: Set to `True` when developing locally to enable the Django Debug Toolbar (DDT). Ensure that `DEBUG` is also set to `True`

Non-secret envs can be added to the `app.json` file. Secrets must be set on Heroku in the `Review Apps` (pipelines' `settings` tab).

### Continuous integration testing

Opening a PR will trigger [Github Action](https://github.com/mozilla/foundation.mozilla.org/actions) continuous integration, which should pass before a PR is deemed good to merge.

### Visual regression testing

[Once a PR has been reviewed and approved a GitHub Action is trigged](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#running-a-workflow-when-a-pull-request-is-approved) that runs visual regression testing using [Percy.io](https://percy.io) (based on Playwright output).
The PR status checks should update to show the result of the visual regression tests.

The visual regression tests are required to pass before a PR can be merged.
This is a change from our previous workflow.
The visual regression tests have been made required to make sure that they have definitely run and passed before a PR is merged.
Since we changed to only trigger the regression tests on PR approval, it could happen that a change is pushed to a PR after it has been approved, which would not trigger the visual regression tests to run again.
That meant the PR status checks would show as passing, but the visual regression tests would not be reported anymore (because they did not trigger again).

Now, the visual regression tests are always listed as a status check, and will always be required to pass before a PR can be merged.
In the situation where a change is pushed to a PR after it has been approved, the visual regression tests will still not trigger again.
It does however seem overkill to require a PR to be re-approved just because a change was pushed to it after it was approved as this will frequently happen due to a rebase.
To run the visual regression tests in such a case, you can add the label `run visual regression tests` to the PR.
This will also trigger the visual regression tests to run algain and update the status checks accordingly.
Note that the **adding** is the trigger.
So if you want to run the tests again (after the label was already added), just remove and re-add the label.

Note that any changes to model fields, field ordering, or factories, will likely result in charges to our testing data, which will result in Percy flagging changes: the test data is based on Python's pseudo-random number generator, which we seed at various points during test data generation, but between those seed points is based on the exact order in which fields are assigned testing data. If the order of assignments changes, or old fields are added/new fields are removed, then the PRNG sequence will be different, and Percy will likely show that there are visual diffs that require sign-off.

It is possible that a PR has Percy-flagged changes, despite the PR not touching model/factory code nor introducing changes to the front-end code. In this case, please alert the engineering team: we've seen this happen in the past and it is unclear why it happens.

For more information on how to work with visual regression tests, see the [Percy docs](https://docs.percy.io/docs).
