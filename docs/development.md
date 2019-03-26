## Development

### Environment Variables

Default environment variables are declared in `env.default`. If you wish to override any of the values, you can create a local `.env` file in the root of the project.

The domain used to fetch static content from Network Pulse can be customized by specifying `PULSE_API_DOMAIN`. By default it uses `network-pulse-api-production.herokuapp.com`.

The URL for fetching static content from the Network API can be customized by specifying `NETWORK_SITE_URL`. By default it uses `https://foundation.mozilla.org`. **NOTE: this variable must include a protocol (such as `https://`)**

### Pipenv and Invoke commands

Pipenv pattern to run Django management commands is:

- `pipenv run python [path to manage.py] [manage.py command] [options]`

For example, you can run your development server that way:

- `pipenv run python network-api/manage.py runserver`

But it's a bit long. So instead, you can use invoke:

- `inv runserver`

### Invoke tasks available:

- `inv -l`: list available invoke tasks
- `inv makemigrations`: Creates new migration(s) for apps
- `inv migrate`: Updates database schema
- `inv runserver`: Start a web server
- `inv setup`: Prepare your dev environment after a fresh git clone
- `inv test`: Run tests
- `inv catch-up`: Install dependencies and apply migrations

For management commands not covered by an invoke tasks, use `inv manage [command]` (example: `inv manage load_fake_data`). You can pass flag and options to management commands using `inv manage [command] -o [positional argument] -f [optional argument]`. For example:
- `inv manage runserver -o 3000`
- `inv manage load_fake_data -f seed=VALUE`
- `inv manage migrate -o news`

### Generating a new set of fake model data

By default, your dev site will use production data (read only!). To load fake model data into your dev site:

- Run `inv manage load_fake_data`
- Replace `NETWORK_SITE_URL` value with `http://localhost:8000` in your `.env` file.

You can empty your database and create a full new set of fake model data using the following command

- `inv manage load_fake_data -o --delete`

Or

- `pipenv run python network-api/manage.py load_fake_data --delete`

You can generate a specific set of fake model data by entering a seed value

- `inv manage load_fake_data -o --delete --seed VALUE`

Or

- `pipenv run python network-api/manage.py load_fake_data --delete --seed VALUE`

Alternatively, the seed value can be specified through the use of the `RANDOM_SEED` environment variable.

If a seed is not provided, a pseudorandom one will be generated and logged to the console. You can share this value with others if you need them to generate the same set of data that you have.

### Landing Page and Campaign links

The `load_fake_data` command will output pages with the following slugs:

- `/`
- `/about/`
- `/styleguide/`
- `/people/`
- `/news/`
- `/initiatives/`
- `/campaigns/single-page/`
- `/campaigns/multi-page/`
- `/opportunity/single-page/`
- `/opportunity/multi-page/`

This list is available on review apps by clicking on `DEV HELP` in the menu or going to `[review app url]/help`.

### Using a copy of the staging database for critical testing

Some development work requires testing changes against "whatever the current production database looks like", which requires having postgresql installed locally (`brew install postgresql` on mac; download and run the official installer for windows; if you use linux/unix, you know how to install things for your favourite flavour, so just do that for postgresql). We backport prod data to staging every week, scrubbing PII, so we'll be creating a copy of that for local testing, too.

The steps involved in cloning the database for local use are as follows:

1) grab a copy of the staging database by running `pg_dump DATABASE_URL > foundation.psql` on the commandline. In this, `DATABASE_URL` is a placeholder, and needs to be replaced with the value found for the `DATABASE_URL` environment variable that is used on heroku, for the staging instance.

_If you are unsure how to get to this value, or how to get to the heroku staging settings, ask someone in the engineering team._

This will take a little while, but once the operation  finishes, open `foundation.psql` in your favourite text/code editor and take note of who the owner is by looking for the following statements:

```
SET search_path = public, pg_catalog;

--
-- Name: clean_user_data(); Type: FUNCTION; Schema: public; Owner: ...... <= we want to know this string
--
```

2) Run `createdb foundation` on the command line so that you have a postgresql database to work with. If you get an error that you already have a database called `foundation`, either create a new database with a new name (and then use that name in the next steps) or delete the old database using `dropdb foundation` before issuing `createdb foundation`.

3) Run `psql foundation` on the command line to connect to that database.

4) Run `CREATE ROLE TheOwnerNameFromTheDBdump WITH SUPERUSER;` in the postgresql command line interface, making sure to have that semi-colon at the end, and making sure NOT to quote the owner name string.

5) Run `\i foundation.psql` in the postgresql command line interface to import the `foundation` database content. Once this finishes you will have an exact copy of the production database set up for local testing.

You will now also need to update your `.env` file to make sure you're using this database, setting `DATABASE_URL=postgres://localhost:5432/foundation`.

If you need to reset this database, rerun step 2 (with `dropdb foundation` as first command) through 5 to get back to a clean copy of the production database.

### Resolving conflicting Django migrations

**AKA: What to do when someone else's migration for the same app lands before yours**

- Create a new, separate local instance of `foundation` per "Setup steps" above.
- Check out your new PR branch locally.
- Delete *all* your PR's migrations and commit the deletion.
- Run `inv makemigrations`
- Commit the newly generated migration.
- Run `inv migrate` to verify and run new migration.
- Push changes to your PR branch.

### Running the project with live front-end reloading

- At the root of the project you can run `npm start`, which will start the server as well as watch tasks for recompiling changes to JS(X) and Sass files.



This project is based on [Wagtail](https://wagtail.io/), which is itself based on Django, so the documentation for both projects applies.
 If you're new to Django, Django official documentation provide a [tutorial](https://docs.djangoproject.com/en/2.0/intro/) and a handful of [topics](https://docs.djangoproject.com/en/2.0/topics/) and [how-to](https://docs.djangoproject.com/en/2.0/howto/) guides to help you get started. If you're completely new to programming, check
 [Django Girls](https://tutorial.djangogirls.org/en/) tutorial.

### Pipenv workflow

Checking [Pipenv documentation](https://docs.pipenv.org/) is highly recommended if you're new to it.

#### Virtual environment

- `pipenv shell` activates your virtual environment and automatically loads your `.env`. Run `exit` to leave it. You don't need to be in your virtual environment to run python commands: Use `pipenv run python [...]` instead.

#### Installing dependencies

- `pipenv install [package name]`

After installing a package, pipenv automatically runs a `pipenv lock` that updates the `pipfile.lock`. You need to add both `pipfile` and `pipfile.lock` to your commit.

#### Updating dependencies

- `pipenv update --outdated` to list dependencies that need to be updated,
- `pipenv update` to update dependencies

If a dependency is updated, pipenv automatically runs a `pipenv lock` that updates the `pipfile.lock`. You need to add both `pipfile` and `pipfile.lock` to your commit.

#### Listing installed dependencies

- `pipenv graph`

### Overriding templates and static content

Sometimes it is necessary to override templates or static js/css/etc assets. In order to track *what* we changed in these files please surround your changes with:

```
# override: start #123
... override code here...
# override: end #123
```

Where `#...` is an issue number pointing to the issue that these changes are being made for.

## Django Migrations

You need to generate a migration file when you add, remove or modify a model. [Django migrations documentation](https://docs.djangoproject.com/en/1.11/topics/migrations/) is a must read on the subject.

You need to follow a special workflow described in the [engineering workflow documentation](./workflow.md) if you intend to remove a field or a model, or if you want to rename or change a field type.
