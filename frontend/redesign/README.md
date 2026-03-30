# Redesign Frontend

Frontend for the redesigned Mozilla Foundation site, built with esbuild and Foundation Framework. Independent from the legacy frontend.

## Visual Regression Testing (Playwright + Percy)

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
