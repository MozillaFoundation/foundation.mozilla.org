## Frontend Workflow for the "Redesign Site"

### Development Mode

- Make sure the `DEBUG` environment variable is set to `True` so that Django and Docker serve updated compiled files correctly.
- Run `docker-compose up` from the root of the codebase (not from `./frontend`).
- Develop as usual.

### CSS

- SCSS files are located in `./foundation_cms/static/scss`.
- These are automatically compiled into `.css` files as part of the build process.

## Frontend commands

- The frontend is composed of two yarn workspaces defined in a root `package.json` file. The two workspaces are
located in `frontend/legacy` and `frontend/redesign`. Running `yarn` commands from the root will trigger
the root scripts defined in the root `package.json` and are helper scripts defined to run for all workspaces.
To run `yarn` commands from an individual workspace, you can `cd` into the workspace, or you can use workspace
syntax from the root directory (for exapmle: `yarn workspace redesign lint`)

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

- Run `yarn format:js` to check whether JavaScript files are correctly formatted.
- Run `yarn format:scss` to check whether SCSS files are correctly formatted.

## Fix Code Formatting

We use [Prettier](https://prettier.io) to enforce consistent code formatting.

From the `./frontend/redesign` directory:

- Run `yarn format` to automatically format JavaScript and SCSS files.

To format them separately:

- Run `yarn format:js` to automatically format JS code
- Run `yarn format:scss` to automatically format SCSS code

## Donate Site

Similar to the Mozilla Festival site, the fake data generator can generate a site structure for the Donation site that can be served under it's own domain.

For local development, the donate site can be found at `donate.localhost:8000`.

## Gotchas

As this is REST API and CMS built on top of Django, there are some "gotcha!"s to keep in mind due to the high level of magic in the Django code base (where things will happen automatically without the code explicitly telling you).

#### **DEBUG=True**

The `DEBUG` flag does all sorts of magical things, to the point where testing with debugging turned on effectively runs a completely different setup compared to testing with debugging turned off. When debugging is on, the following things happen:

- Django bypasses the `ALLOWED_HOST` restrictions, which again can lead to `400 Bad Request` errors in `DEBUG=False` setting.
- Rather than HTTP error pages, Django will generate stack traces pages that expose pretty much all environment variables except any that match certain substrings such as `KEY`, `PASS`, etc. for obvious security reasons.
- ...there are probably more gotchas just for `DEBUG` so if you find any please add them to this list.

## Translations

Translations of UI strings (from the Django and React apps) are stored in [the fomo-l10n repository](https://github.com/mozilla-l10n/fomo-l10n). Translations are happening in Pontoon, in multiple projects: [Foundation website](https://pontoon.mozilla.org/projects/mozilla-foundation-website/), [\*Privacy Not Included](https://pontoon.mozilla.org/projects/privacy-not-included/) and [Mozilla Festival](https://pontoon.mozilla.org/projects/mozilla-festival/).

The latest source strings are regularly exposed to Pontoon by a Localization PM using the following process:

### Initial setup:
- Clone the [`fomo-l10n`](https://github.com/mozilla-l10n/fomo-l10n) repository locally.
- Set the `LOCAL_PATH_TO_L10N_REPO` variable in your `.env` file. Use the absolute path to your copy of the `fomo-l10n` repository and include the trailing slash. E.g. `LOCAL_PATH_TO_L10N_REPO=/Users/username/Documents/GitHub/fomo-l10n/`

### Exposing latest source strings:
- Make sure your local repositories of `fomo-l10n` and `foundation.mozilla.org` are matching the latest revision from main.
- Run `inv docker-makemessages` from your `foundation.mozilla.org` repository.
- Files should have been updated in your `fomo-l10n` repository. You can now create a pull-request.

### Getting the latest translations for local dev

Latest translations are uploaded to S3. To get them, run:
- `curl -o translations.tar https://foundation-site-translations.s3.amazonaws.com/translations.tar`
- `tar -C foundation_cms -xvf translations.tar`

You don't need to run `compilemessages` and it works for both pipenv or docker workflows.

The `translations_github_commit_[...]` file from the archive is only used for debug purposes on Heroku. It can be safely deleted if needed.

## Contributing

We love contributors, but the team maintaining this project is small and not structured to significantly support new and inexperienced contributors. If there's an unassigned issue that catches your eye, feel free to open a PR for it, but keep in mind our support will be limited. We usually don't have the capacity to walk you through the process of spinning up the project, opening a PR or describing what the solution to the issue could be.
