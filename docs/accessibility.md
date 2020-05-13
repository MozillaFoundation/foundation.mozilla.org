# Accessibility Testing using Cypres and Axe

This codebase comes with accessibility (a11y) testing in the form of [Axe](https://www.deque.com/axe/) combined with [Cypress](https://www.cypress.io/).

In order to set up accessibility testing locally, clone and install the project as per the instructions, including making sure the Docker image is fully set up, and then run the Cypress/Axe installs using:

```
npm run cypress:install
```

Note that this should be run locally, _outside of Docker_, which means you will also need to run the regular npm installs using:

```
npm install
```

Finally, note that the cypress installation can take quite a while, so be prepared to make some coffee or tea, and maybe even a sandwich or some ramen.


## Running Cypress Accessibility Tests

Once everything is installed, the a11y tests can be invoked by running the command:

```
npm run cypress:a11y
```

Provided that all the Cypress dependencies are installed, this kicks off an automated test run for all tests in the a11y test script using your locally instapped cypress, connecting to the server running inside of Docker.

#### Failures

When tests fail, the `./cypress/screenshots` directory will contain one screenshot per failed test, with information on what actually went wrong, compared to the summar error stack trace on the console.

#### Tests that use `it.skip(...)`

Some tests may be set to "skip", which means that there is a test, but Cypress is instructed to pass over it rather than running it. In the Cypress UI this will look like the test has stalled: it probably hasn't. Look in the `./cypress/integration/a11y-tests.js` file to see if the test(s) in question is/are marked as skipped.

## Manual Cypress Testing using the Cypress Desktop UI

In addition to automated testing, you can also tell Cypress to start up its UI, for interactive test running. To do so, run:

```
npm run cypress:test:manual
```
## Manual Accessibility Testing using the Browser

You can also perform manual a11y analysis of any webpage by pointing either Firefox or Chrome at a localhost:8000 page and using the [Axe web extension](https://www.deque.com/axe/axe-for-web), which enables a new tab in dev tools for analysing pages. For general issue work, this is the easier way to test accessibility for single pages or small sets of pages, compared to running the full battery of tests using Cypress.
