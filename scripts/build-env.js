let dotenv = require(`dotenv`);
let shelljs = require(`shelljs`);

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
let finalEnv = Object.assign(defaultEnv, localEnv);

// Write JSON based env
shelljs.echo(JSON.stringify(finalEnv, null, 2)).to(`env.json`);
