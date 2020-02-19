# Accessibility Testing using Cypres and Axe

This codebase comes with accessibility (a11y) testing in the form of [Axe](https://www.deque.com/axe/) combined with [Cypress](https://www.cypress.io/).

In order to set up accessibility testing locally, clone and install the project as per the instructions, including making sure the Docker image is fully set up, and then run the Cypress/Axe installs using:

```
npm run cypress:install
```

Note that this should be run locally, _outside of Docker_. Also note that this will take quite a while to install, so be prepared to make some coffee/tea and maybe even a sandwich.

## Running Cypress Accessibility Tests

Once everything is installed, the a11y tests can be invoked by first making sure the server is running in docker, following the instructions for a normal build run, and then once the server is up and running, separately running the command:

```
npm run build:dev:a11y
```

This checks that all the Cypress dependencies are installed, and then kicks off a dev-rebuild specifically for a11y testing, and start up cypress locally (outside of docker). Once open, select the a11y tests, and Cypress should automatically start running them.

#### Tests that use `it.skip(...)`

Some tests may be set to "skip", which means that there is a test, but Cypress is instructed to pass over it rather than running it. In the Cypress UI this will look like the test has stalled: it probably hasn't. Look int the `./cypress/integration/a11y-tests.js` file to see if the test(s) in question is/are marked as skipped.

## Manual Browser-testing of Accessibility

You can also perform manual a11y analysis by pointing either Firefox or Chromne at a localhost page and using the [Axe web extension](https://www.deque.com/axe/axe-for-web), which enables a new tab in dev tools for analysing pages. For general issue work, this is the easier way to test accessibility for single pages or small sets of pages, compared to running the full batter of tests using Cypress.

## Running Cypress Unattended

In order to run all Cypress tests without using the Cypress UI, the following command can be used:

```
npm run cypress:test:a11y
```

This will run through all tests on the command line and report any failures through logs as well as a non-zero process exit code.
