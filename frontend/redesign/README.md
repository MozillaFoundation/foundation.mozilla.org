# Redesign Frontend

Frontend for the redesigned Mozilla Foundation site, built with esbuild and Foundation Framework. Independent from the legacy frontend.

## Development Workflow

### Development Mode

- Make sure the `DEBUG` environment variable is set to `True` so that Django and Docker serve updated compiled files correctly.
- Run `docker compose up` from the root of the codebase (not from `./frontend`).
- Develop as usual.

### CSS

- SCSS files are located in `./foundation_cms/static/scss`.
- These are automatically compiled into `.css` files as part of the build process.

## Check Linting Error

From the `./frontend/redesign` directory:

- Run `yarn lint` to check JavaScript and SCSS files for linting errors.

To lint separately:

- Run `yarn lint:js` to check JavaScript files for linting errors.
- Run `yarn lint:scss` to check SCSS files using Stylelint.

## Fix Linting Error

From the `./frontend/redesign` directory:

- Run `yarn fix` to automatically fix JavaScript and SCSS linting errors.

To fix them separately:

- Run `yarn fix:js` to automatically fix fixable linting issues using ESLint.
- Run `yarn fix:scss` to automatically fix SCSS linting issues.

## Check Code Formatting

We use [Prettier](https://prettier.io) to enforce consistent code formatting.

From the `./frontend/redesign` directory:

- Run `yarn check-format` to check whether JavaScript and SCSS files are correctly formatted.

To check them separately:

- Run `yarn check-format:js` to check whether JavaScript files are correctly formatted.
- Run `yarn check-format:scss` to check whether SCSS files are correctly formatted.

## Fix Code Formatting

We use [Prettier](https://prettier.io) to enforce consistent code formatting.

From the `./frontend/redesign` directory:

- Run `yarn format` to automatically format JavaScript and SCSS files.

To format them separately:

- Run `yarn format:js` to automatically format JS code
- Run `yarn format:scss` to automatically format SCSS code

## Unit Testing (Vitest)

Unit tests run against vanilla JS modules under `foundation_cms/static/js` using [Vitest](https://vitest.dev/) with a jsdom environment, so they can exercise DOM reads/writes and event dispatching without a real browser.

### Run tests locally

| Script | Description |
| --- | --- |
| `yarn workspace redesign test` | Run the suite once, with coverage |
| `yarn workspace redesign test:watch` | Watch mode, reruns on file save |

### Adding new tests

Colocate test files as `*.test.js` next to the module they cover, e.g. `foundation_cms/static/js/blocks/pillar_card_set.test.js` tests `pillar_card_set.js` in the same directory.

## Visual Regression Testing (Playwright + Percy)

This covers the redesign frontend. The legacy frontend has its own separate Playwright + Percy visual regression suite (see [foundation_cms/legacy_apps/README.md](../../foundation_cms/legacy_apps/README.md#visual-regression-tests)).

### Prerequisites

1. Install dependencies from the repo root:
   ```sh
   yarn install
   ```

2. Install Playwright browsers:
   ```sh
   yarn workspace redesign playwright:install
   ```

3. Start the Django dev server (the tests hit `http://localhost:8000`):
   ```sh
   python manage.py runserver
   ```

### Run Playwright locally (no Percy)

Takes screenshots and saves them to `frontend/redesign/tests/screenshots/`.

```sh
yarn workspace redesign playwright test ./tests/visual.spec.js
```

### Adding new URLs

Add entries to [`tests/redesign-urls.js`](tests/redesign-urls.js). Each key becomes the test/snapshot name, and the value is the path:

```js
const RedesignURLs = {
  Homepage: "/",
};
```

When adding pages from new sections of the site, also update the workflow trigger paths in [`.github/workflows/visual-regression-testing-redesign.yml`](../../.github/workflows/visual-regression-testing-redesign.yml).
