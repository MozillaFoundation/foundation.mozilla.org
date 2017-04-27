let dotenv = require(`dotenv`);
let shelljs = require(`shelljs`);

// Pull in env defaults
let defaultEnv = dotenv.parse(shelljs.cat(`defaults.env`));

// Check for local env overrides
let localEnv = shelljs.test(`-f`, `.env`) ? dotenv.parse(shelljs.cat(`.env`)) : {};

// Merge overrides into defaults
let finalEnv = Object.assign(defaultEnv, localEnv);

// Write JSON based env
shelljs.echo(JSON.stringify(finalEnv, null, 2)).to(`env.json`);
