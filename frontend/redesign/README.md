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

| Script                               | Description                       |
| ------------------------------------ | --------------------------------- |
| `yarn workspace redesign test`       | Run the suite once, with coverage |
| `yarn workspace redesign test:watch` | Watch mode, reruns on file save   |

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

Takes screenshots and saves them to Playwright's `test-results/` directory.
Set `PLAYWRIGHT_OUTPUT_DIR` to an absolute path to keep artifacts elsewhere.

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

### Cosmos reskin spike

`tests/reskin-visual.spec.js` adds two focused General Page fixtures to the
existing Percy command. It captures the empty page and the populated page
with its accordion closed and open, each at 1280px and 375px (six snapshots).
Each browser viewport matches the width requested for its Percy snapshot.
The existing broad General Page and other page captures remain in the suite.

On a fresh development/CI database, `python manage.py load_redesign_data`
includes these pages. If the default site already has a redesign homepage,
`python manage.py load_visual_regression_data` creates only the two missing
pages. It never changes existing pages, navigation, footer, users or images.
It scopes lookup to the parent and locale, and refuses a conflicting page type.
Existing edited fixtures are preserved; a failed smoke assertion should be
investigated instead of silently overwriting their content.

- `/en/visual-regression-empty/`: real page shell, navigation, footer and
  assets; no hero or body blocks. The page title remains visible.
- `/en/visual-regression-components/`: a Cosmos section containing fixed
  text, primary/secondary links and two accordion items. At the spike's base
  (`8cbe2f288` on `site-refresh-2026`), the section master is ported to Cosmos;
  buttons, accordion and shell retain the implementations on that branch.
  This is preparation for subsequent reskins, not proof those reskins are
  complete. No unmerged component PR is required.

Before capture, the suite checks HTTP 200, URL/title, the General Page shell,
hero absence, navigation/footer, loaded first-party assets and web fonts,
horizontal overflow, expected body content, and accordion state. Section
spacing is checked against the ported LP reference in
`foundation_cms/static/scss/cosmos/elements/layout/_section-master.scss`
(LP `31accfd52e`, Figma `9470:11913`): desktop 200px vertical/148px horizontal
padding and 72px rhythm; mobile 64px/20px padding and 48px rhythm.

The browser uses a fixed date, locale, timezone, color scheme, scale and
viewport. Third-party scripts are blocked to exclude widgets/analytics.
First-party page markup and assets are not mocked. Real navigation/footer
content comes from the database, so use the same seeded database when
comparing runs; arbitrary editorial changes are expected visual differences.
The suite waits for images, fonts, accordion completion and scroll position,
rather than network-idle or fixed sleeps.

Run the focused smoke/capture suite without a Percy token:

```sh
PLAYWRIGHT_OUTPUT_DIR=/absolute/path/to/artifacts yarn workspace redesign visual:reskin
```

Local runs check readiness and behavior and save diagnostic PNGs. They do not
compare images or create visual baselines. Percy handles visual comparison
and baseline review through the existing redesign project.

### CI and baseline review recommendation

Keep Percy as the shared review system. The existing workflow seeds a fresh
database and runs both suites through `yarn workspace redesign percy`, using
`PERCY_TOKEN_REDESIGN`. Its current triggers are the redesign label, approved
PR reviews touching redesign paths, and pushes to `main`/`site-refresh-2026`.
For this spike, retain those triggers. Before making the check required,
consider rerunning on `synchronize` for PRs carrying the redesign label so
later commits cannot rely on an earlier visual result. Keep refresh work
targeted at `site-refresh-2026` and verify Percy's selected comparison branch.

Review all six initial snapshots at both widths against the intended design,
not just against each other. Check section metrics against the cited LP/Figma
reference, then have the design/component owner assess typography, colors,
shell and component states. Record any deliberately transitional styling.
Missing fonts/assets, clipped content, unexpected blank regions and stale
component code must be resolved or explicitly tracked before approval.
Recheck component design references when their reskin PRs land.

Only an authorized reviewer should approve the initial Percy baseline and
intentional diffs. Do not auto-approve from a successful Playwright run, a
new snapshot, or a local smoke result. Percy dry-runs validate snapshot
collection only; they do not upload a build or verify cloud rendering,
comparison-branch selection or approval behavior.
