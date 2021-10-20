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

const inDir = `./source/js/`;
const outDir = `./network-api/networkapi/frontend/_js/`;

const sources = {
  main: `main.js`,
  mozfest: `foundation/pages/mozfest/index.js`,
  "callpower": `foundation/pages/callpower.js`,
  "directory-listing-filters": `foundation/pages/directory-listing-filters.js`,
  "bg-main": `buyers-guide/bg-main.js`,
  polyfills: `polyfills.js`,
};

const base = {
  bundle: true,
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
  inject: [`esbuild.react.shim.js`],
};

Object.entries(sources).map(([name, source]) => {
  const opts = Object.assign({}, base);
  opts.entryPoints = [path.join(inDir, source)];
  opts.outfile = `${path.join(outDir, name)}.compiled.js`;
  return build(opts);
});
