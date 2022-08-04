const fs = require("fs");
const { execSync } = require(`child_process`);

const deleteDatabase = process.argv.includes(`--delete`);
const silent = { stdio: [`ignore`, `ignore`, `ignore`] };
const PROD_APP = `foundation-mozilla-org`;
const STAGE_APP = `foundation-mofostaging-net`;
const APP = process.argv.includes(`--prod`) ? PROD_APP : STAGE_APP;

if (APP === STAGE_APP) {
  console.log(
    `Running db copy for staging, run with --prod to run for production`
  );
}

const HEROKU_OUTPUT = run(`heroku config:get DATABASE_URL -a ${APP}`);
const HEROKU_TEXT = HEROKU_OUTPUT.toString().replaceAll(`\n`, ` `);
const URL_START = HEROKU_TEXT.indexOf(`postgres://`);
const DATABASE_URL = HEROKU_TEXT.substring(URL_START).trim();
const ROLE = DATABASE_URL.match(/postgres:\/\/([^:]+):/)[1];
const DUMP_FILE = `${ROLE}.db.archive`;
const DB_FLAGS = `-hpostgres -Ufoundation`;

/**
 * Exec a command and return its output as plain string
 */
function run(cmd, ignoreThrows = false, opts = {}) {
  try {
    return execSync(cmd, opts).toString();
  } catch (e) {
    if (ignoreThrows) return e.toString();
    process.exit(1);
  }
}

/**
 * Run a command in the postgres docker container
 */
function postgres(cmd, ignoreThrows = false) {
  cmd = `docker exec ${IMAGE_NAMES.POSTGRES} ${cmd}`;
  return run(cmd, ignoreThrows);
}

function getContainerNames() {
  return run(`docker ps`)
    .split(`\n`)
    .map((v) => v.match(/\s(\S+)$/g))
    .filter(Boolean)
    .map((v) => v[0].trim())
    .reduce((a, v) => {
      if (!v) return a;
      if (v.includes(`backend`)) a.BACKEND = v;
      if (v.includes(`postgres`)) a.POSTGRES = v;
      return a;
    }, {});
}

function stopContainers() {
  const IMAGE_NAMES = getContainerNames();

  const backend = IMAGE_NAMES.BACKEND;
  if (backend) {
    console.log(`Stopping ${backend}`);
    run(`docker stop ${backend}`, true, silent);
  }

  const postgres = IMAGE_NAMES.POSTGRES;
  if (postgres) {
    console.log(`Stopping ${postgres}`);
    run(`docker stop ${postgres}`, true, silent);
  }
}

// ======================== //
//  Our script starts here  //
// ======================== //

console.log(`Making sure no docker containers are running...`);
stopContainers();

console.log(`Starting postgres docker image...`);
run(`docker-compose up -d postgres`, true, silent);

console.log(`Starting backend docker image...`);
run(`docker-compose up -d backend`, true, silent);

console.log(`Getting running image names...`);
const IMAGE_NAMES = getContainerNames();

if (!fs.existsSync(DUMP_FILE)) {
  console.log(`Downloading ${APP} database (this may take a while)...`);
  postgres(`pg_dump -F c ${DATABASE_URL} > ${DUMP_FILE}`);
} else {
  console.log(`Found local ${APP} database file, skipping download...`);
}

console.log(`Resetting db...`);
postgres(`dropdb ${DB_FLAGS} --if-exists wagtail --force`);
postgres(`createdb ${DB_FLAGS} wagtail`);

console.log(`Building user roles...`);
[ROLE, `datastudio`, `datagrip-cade`].forEach((role) =>
  postgres(`createuser ${DB_FLAGS} -s ${role}`, true)
);

console.log(`Importing database snapshot...`);
run(`docker cp ${DUMP_FILE} ${IMAGE_NAMES.POSTGRES}:/`);
// Based on the Heroku docs for restoring to local database:
// https://devcenter.heroku.com/articles/heroku-postgres-import-export#restore-to-local-database
postgres(`pg_restore ${DB_FLAGS} -dwagtail --no-acl --no-owner ${DUMP_FILE}`);

console.log(`Updating site bindings...`);
run(`inv manage fix_local_site_bindings`, true, silent);

console.log(`Creating admin:admin superuser account...`);
run(`inv createsuperuser`, true, silent);

console.log(`Migrating database to match current branch migrations...`);
run(
  `docker exec ${IMAGE_NAMES.BACKEND} ./dockerpythonvenv/bin/python network-api/manage.py migrate`
);

console.log(`Stopping docker images...`);
run(`docker-compose down`, true, silent);

if (deleteDatabase) {
  console.log(`Running cleanup`);
  fs.unlinkSync(DUMP_FILE);
}

console.log(`All done.`);
