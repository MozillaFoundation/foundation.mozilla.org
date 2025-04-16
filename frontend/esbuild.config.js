const { context, build } = require("esbuild");
const path = require("path");

const arg = process.argv.indexOf("--node-env");
const mode =
  arg > 0 ? process.argv[arg + 1] : process.env.NODE_ENV || "development";
const inProduction = mode === "production";

console.log("ESBuild running in production mode?", inProduction);

const inDir = "../foundation_cms/static/js/";
const outDir = "../foundation_cms/static/compiled/_js";

const sources = {
  redesign_main: {
    source: "redesign_main.js",
    jsx: false,
    bundle: true,
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

// We use a for...of loop instead of forEach because forEach doesn't handle async/await properly.
// forEach won't wait for the async function to finish before moving to the next item,
// which can cause unexpected behavior in sequential build tasks like this.
async function runBuilds() {
  for (const [name, config] of Object.entries(sources)) {
    const opts = {
      ...base,
      entryPoints: [path.join(inDir, config.source)],
      outfile: path.join(outDir, `${name}.compiled.js`),
      bundle: config.bundle,
    };

    if (config.jsx) {
      opts.jsx = config.jsx;
    }

    if (inProduction) {
      await build(opts);
      console.log(`Built ${name}`);
    } else {
      const ctx = await context(opts);
      await ctx.watch();
      console.log(`Watching ${name}...`);
    }
  }
}

runBuilds().catch((err) => {
  console.error("Build failed:", err);
  process.exit(1);
});
