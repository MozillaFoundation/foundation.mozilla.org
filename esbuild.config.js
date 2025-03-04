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
const { context, build } = require(`esbuild`);
const path = require(`path`);

const arg = process.argv.indexOf(`--node-env`);
const mode =
  arg > 0 ? process.argv[arg + 1] : process.env.NODE_ENV || `development`;
const inProduction = mode === `production`;

console.log(`ESBuild running in production mode?`, inProduction);

const inDir = `./frontend/legacy_source/js/`;
const outDir = `./frontend/legacy_compiled/_js/`;

const sources = {
  main: {
    source: `main.js`,
    jsx: "automatic",
    bundle: true,
  },
  mozfest: {
    source: `foundation/pages/mozfest/index.js`,
    jsx: "automatic",
    bundle: true,
  },
  callpower: {
    source: `foundation/pages/callpower.js`,
    bundle: true,
  },
  "directory-listing-filters": {
    source: `foundation/pages/directory-listing-filters.js`,
  },
  "bg-main": {
    source: `buyers-guide/bg-main.js`,
    jsx: "automatic",
    bundle: true,
  },
  "bg-search": {
    source: `buyers-guide/search.js`,
    bundle: true,
  },
  "bg-editorial-content-index": {
    source: `buyers-guide/editorial-content-index.js`,
    bundle: true,
  },
  "libraries-library-page": {
    source: `foundation/pages/libraries-library-page.js`,
    bundle: true,
  },
  polyfills: {
    source: `polyfills.js`,
  },
};

const base = {
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

const opts = Object.assign({}, base);

Object.entries(sources).forEach(async ([name, { source, jsx, bundle }]) => {
  if (jsx) {
    opts.jsx = jsx;
  }
  if (bundle) {
    opts.bundle = true;
  }
  opts.entryPoints = [path.join(inDir, source)];
  opts.outfile = `${path.join(outDir, name)}.compiled.js`;

  if (inProduction) {
    return build(opts);
  } else {
    let ctx = await context(opts);
    await ctx.watch();
  }
});
