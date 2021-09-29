const fs = require("fs");
const { execSync } = require(`child_process`);

const keepDatabase = process.argv.includes(`--keep`);
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
 * ...
 */
function run(cmd, ignoreThrows = false, opts = {}) {
  try {
    return execSync(cmd, opts);
  } catch (e) {
    if (ignoreThrows) return e.toString();
    throw e;
  }
}

/**
 * ...
 */
function docker(cmd, ignoreThrows = false) {
  cmd = `docker exec foundation_postgres_1 ${cmd}`;
  return run(cmd, ignoreThrows);
}

console.log(`Starting postgres docker image...`);
run(`docker-compose up -d postgres`, true, silent);

console.log(`Starting backend docker image...`);
run(`docker-compose up -d backend`, true, silent);

console.log(`Downloading ${APP} database (this may take a while)...`);
if (!fs.existsSync(DUMP_FILE)) {
  docker(`pg_dump -F c ${DATABASE_URL} > ${DUMP_FILE}`);
}

console.log(`Resetting db...`);
docker(`dropdb ${DB_FLAGS} --if-exists wagtail`);
docker(`createdb ${DB_FLAGS} wagtail`);

console.log(`Building user roles...`);
[ROLE, `datastudio`, `datagrip-cade`].forEach((role) =>
  docker(`createuser ${DB_FLAGS} -s ${role}`, true)
);

console.log(`Importing snapshot...`);
run(`docker cp ${DUMP_FILE} foundation_postgres_1:/`);
docker(`pg_restore ${DB_FLAGS} -dwagtail ${DUMP_FILE}`);

console.log(`Creating admin:admin superuser account...`);
run(
  [
    `docker exec foundation_backend_1`,
    `./dockerpythonvenv/bin/python network-api/manage.py shell -c`,
    `"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"`,
  ].join(` `),
  true,
  silent
);


console.log(`Stopping docker images...`);
run(`docker-compose down`, true, silent);

if (!keepDatabase) {
  console.log(`Running cleanup`);
  fs.unlinkSync(DUMP_FILE);
}

console.log(`All done.`);
