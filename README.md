# Frontend Workflow for the "Redesign Site"

## Development Mode

- Make sure the `DEBUG` environment variable is set to `True` so that Django and Docker serve updated compiled files correctly.
- Run `docker-compose up` from the root of the codebase (not from `./frontend`).
- Develop as usual.

## CSS

- SCSS files are located in `./foundation_cms/static/scss`.
- These are automatically compiled into `.css` files as part of the build process.

## Linting

From the `./frontend` directory:

- Run `yarn lint` to check JavaScript and SCSS files for linting errors.

To lint separately:

- Run `yarn lint:js` to check JavaScript files for linting errors.
- Run `yarn lint:scss` to check SCSS files using Stylelint.

## Fix Linting Error

From the `./frontend` directory:

- Run `yarn fix` to automatically fix JavaScript and SCSS linting errors.

To fix them separately:

- Run `yarn fix:js` to automatically fix fixable linting issues using ESLint.
- Run `yarn fix:scss` to automatically fix SCSS linting issues.

## Code Formatting

We use [Prettier](https://prettier.io) to enforce consistent code formatting.

From the `./frontend` directory:

- Run `yarn format` to automatically format JavaScript and SCSS files.

To format them separately:

- Run `yarn format:js` to automatically format JS code
- Run `yarn format:scss` to automatically format SCSS code
