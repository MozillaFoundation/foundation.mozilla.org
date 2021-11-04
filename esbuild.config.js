/**
 * This is not technically a "config", but the actual run script that
 * invokes ESBuild (https://esbuild.github.io) on the various libraries
 * that we need bundled and written to our frontend's js directory.
 *
 * As a normal script, this should be invoked using node, and it can
 * take a runtime argument `--node-env` followed by either the string
 * "production" or "development" so that process.env.NODE_ENV in our
 * code gets interpreted correctly.
 */
const { build } = require(`esbuild`);
const path = require(`path`);

const arg = process.argv.indexOf(`--node-env`);
const mode =
  arg > 0 ? process.argv[arg + 1] : process.env.NODE_ENV || `development`;
const inProduction = mode === `production`;

console.log(`ESBuild running in production mode?`, inProduction);

const inDir = `./source/js/`;
const outDir = `./network-api/networkapi/frontend/_js/`;

const sources = {
  main: {
    source: `main.js`,
    react: true,
    bundle: true,
  },
  mozfest: {
    source: `foundation/pages/mozfest/index.js`,
    react: true,
    bundle: true,
  },
  callpower: {
    source: `foundation/pages/callpower.js`,
  },
  "directory-listing-filters": {
    source: `foundation/pages/directory-listing-filters.js`,
  },
  "bg-main": {
    source: `buyers-guide/bg-main.js`,
    react: true,
    bundle: true,
  },
  "bg-search": {
    source: `buyers-guide/search.js`,
  },
  polyfills: {
    source: `polyfills.js`,
  },
};

const base = {
  watch: !inProduction,
  sourcemap: !inProduction,
  minify: inProduction,
  loader: {
    ".js": "jsx",
    ".jsx": "jsx",
  },
  define: {
    "process.env.NODE_ENV": JSON.stringify(mode),
  },
};

Object.entries(sources).map(([name, { source, react, bundle }]) => {
  const opts = Object.assign({}, base);
  if (react) {
    opts.inject = [`esbuild.react.shim.js`];
  }
  if (bundle) {
    opts.bundle = true;
  }
  opts.entryPoints = [path.join(inDir, source)];
  opts.outfile = `${path.join(outDir, name)}.compiled.js`;
  return build(opts);
});
