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
import { context, build } from "esbuild";
import path from "path";
import { fileURLToPath } from "url";

// __dirname and __filename emulation for ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const arg = process.argv.indexOf("--node-env");
const mode =
  arg > 0 ? process.argv[arg + 1] : process.env.NODE_ENV || "development";
const inProduction = mode === "production";

console.log("ESBuild running in production mode?", inProduction);

const inDir = path.resolve(__dirname, "../../foundation_cms/legacy_apps/static/js/");
const outDir = path.resolve(__dirname, "../../foundation_cms/legacy_apps/static/compiled/_js/");

const sources = {
  main: {
    source: "main.js",
    jsx: "automatic",
    bundle: true,
  },
  mozfest: {
    source: "foundation/pages/mozfest/index.js",
    jsx: "automatic",
    bundle: true,
  },
  callpower: {
    source: "foundation/pages/callpower.js",
    bundle: true,
  },
  "directory-listing-filters": {
    source: "foundation/pages/directory-listing-filters.js",
  },
  "bg-main": {
    source: "buyers-guide/bg-main.js",
    jsx: "automatic",
    bundle: true,
  },
  "bg-search": {
    source: "buyers-guide/search.js",
    bundle: true,
  },
  "bg-editorial-content-index": {
    source: "buyers-guide/editorial-content-index.js",
    bundle: true,
  },
  "libraries-library-page": {
    source: "foundation/pages/libraries-library-page.js",
    bundle: true,
  },
  polyfills: {
    source: "polyfills.js",
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

async function run() {
  for (const [name, { source, jsx, bundle }] of Object.entries(sources)) {
    const opts = {
      ...base,
      entryPoints: [path.join(inDir, source)],
      outfile: path.join(outDir, `${name}.compiled.js`),
      bundle: !!bundle,
    };

    if (jsx) {
      opts.jsx = jsx;
    }

    if (inProduction) {
      await build(opts);
      console.log(`Built ${name}.compiled.js`);
    } else {
      const ctx = await context(opts);
      await ctx.watch();
      console.log(`Watching ${name}.compiled.js...`);
    }
  }
}

run().catch((err) => {
  console.error("Build failed:", err);
  process.exit(1);
});
