let dotenv = require(`dotenv`);
let shelljs = require(`shelljs`);

const ENV_WHITELIST = [
  `PULSE_API_DOMAIN`,
  `PULSE_DOMAIN`,
  `NETWORK_SITE_URL`,
  `TARGET_DOMAIN`,
  `SHOW_TAKEOVER`
];

// Pull in env defaults
let defaultEnv = dotenv.parse(shelljs.cat(`env.default`));

// Check for process env variables and override defaults where found
Object.keys(defaultEnv).forEach((key) => {
  if (process.env[key]) {
    defaultEnv[key] = process.env[key];
  }
});

// Check for local .env overrides (these take highest priority)
let localEnv = shelljs.test(`-f`, `.env`) ? dotenv.parse(shelljs.cat(`.env`)) : {};

// Merge overrides into defaults
let mergedEnv = Object.assign(defaultEnv, localEnv);

// Filter env variables using a whitelist (ENV_WHITELIST)
let finalEnv = {};

Object.keys(mergedEnv).forEach((key) => {
  if (ENV_WHITELIST.includes(key)) {
    finalEnv[key] = mergedEnv[key];
  }
});

// Write JSON based env
shelljs.echo(JSON.stringify(finalEnv, null, 2)).to(`env.json`);
