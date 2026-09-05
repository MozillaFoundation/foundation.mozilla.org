# Legacy Apps

Django apps that predate the Redesign and still power a couple of standalone site sections. For project setup, Python unit tests, and general docs, see the [root README.md](../../README.md). The legacy frontend's own Playwright/Percy test setup is documented below.

## Mozilla Festival

The fake data generator can generate a site structure for the Mozilla Festival that can be served under it's own domain, or in the case of review apps on Heroku, where we're limited to a single domain, as a sub-directory of the main foundation site, at `{review_app_host}/mozilla-festival`.

In order to access the Mozilla Festival site locally on a different domain than the main Foundation site, you'll need to edit your hosts file (`/etc/hosts` on *nix systems, `C:\Windows\System32\Drivers\etc\hosts` on Windows) to allow you to access the site at `mozfest.localhost:8000`. To enable this, add the following line to your hosts file: `127.0.0.1 mozfest.localhost`

Ticket purchases are implemented using a third-party integration with [Tito](https://ti.to/).
A `Tito Event` snippet can be created for each event for which registration is needed. A `TitoWidget` Streamfield block can be used to place a button on a page to open the Tito widget, linked to a specific `Tito Event`.
A `Tito Event` needs a security token and newsletter question ID which can be found in the Customize -> Webhooks section of the Tito admin dashboard for the event.
A webhook (Django view) receives requests from Tito when a ticket is completed in order to sign users up for the Mozilla newsletter.

## Donate Site

Similar to the Mozilla Festival site, the fake data generator can generate a site structure for the Donation site that can be served under it's own domain.

For local development, the donate site can be found at `donate.localhost:8000`.

## Linting and Formatting

From the `./frontend/legacy` directory (or `yarn workspace legacy <script>` from the repo root):

- Run `yarn lint` to check JavaScript and SCSS files for linting errors.
- Run `yarn fix` to auto-fix JavaScript (ESLint) and SCSS (Stylelint) issues.

Unlike the redesign frontend, there's no separate Prettier check-only step wired up here, `yarn fix` handles both linting and formatting fixes together.

## Testing

The legacy frontend's Playwright/Percy tests live under `frontend/legacy/tests`, and its scripts run through the `legacy` yarn workspace. The redesign frontend has its own separate Vitest and Playwright/Percy setup (see [frontend/redesign/README.md](../../frontend/redesign/README.md)).

### Integration tests

Integration testing is done using [Playwright](https://playwright.dev/), with the integration tests found in `frontend/legacy/tests/integration`.

Install the Playwright browsers once with `yarn workspace legacy playwright:install`, then run the integration suite with `yarn workspace legacy playwright`, with `docker compose up` running in a secondary terminal.

In order to run the same tests as will run during CI testing, make sure that `RANDOM_SEED=530910203` is set in your `.env` file, and that your local database is a new db based on that seed (`inv new-db`).

#### URL checker

URL checker can be initiated by running `docker compose up` in one terminal and running `yarn workspace legacy playwright:legacy:urls` in a secondary terminal. It checks to see if visiting the URLs listed in [`frontend/legacy/tests/foundation-urls.js`](https://github.com/MozillaFoundation/foundation.mozilla.org/blob/main/frontend/legacy/tests/foundation-urls.js) and [`frontend/legacy/tests/mozfest-urls.js`](https://github.com/MozillaFoundation/foundation.mozilla.org/blob/main/frontend/legacy/tests/mozfest-urls.js) returns an OK response (i.e., status 200). Note that the URL lists in these two files are not complete and will require updates. We will also need to expand the lists to include PNI and Donate URLs.

### Visual regression tests

We also use Playwright in combination with Browserstack's [Percy](https://percy.io/) to perform visual regression testing for PRs, using `frontend/legacy/tests/visual.spec.js` as screenshot baseline. Run it locally with `yarn workspace legacy percy`.

Visual regression tests are run after a pull request review has been approved.

This covers the legacy frontend. The redesign frontend has its own separate Playwright + Percy visual regression suite (see [frontend/redesign/README.md](../../frontend/redesign/README.md#visual-regression-testing-playwright--percy)).

### Accessibility tests

Accessibility tests are currently unavailable but will use [axe-playwright](https://www.npmjs.com/package/axe-playwright) when the switchover from Cypress to Playwright is complete.
