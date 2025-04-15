# Frontend Workflow for the "Redesign Site"

## Development Mode

- Make sure the `DEBUG` environment variable is set to `True` so that Django and Docker serve updated compiled files correctly.
- Run `docker-compose up` from the root of the codebase (not from `./frontend`).
- Develop as usual.

## CSS

- SCSS files are located in `./foundation_cms/static/scss`.
- These are automatically compiled into `.css` files as part of the build process.
