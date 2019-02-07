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
