# Redesign Frontend

Frontend for the redesigned Mozilla Foundation site, built with esbuild and Foundation Framework. Independent from the legacy frontend.

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
