const { context, build } = require("esbuild");
const path = require("path");

const arg = process.argv.indexOf("--node-env");
const mode =
  arg > 0 ? process.argv[arg + 1] : process.env.NODE_ENV || "development";
const inProduction = mode === "production";

console.log("ESBuild running in production mode?", inProduction);

const inDir = "../foundation_cms/static/js";
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

// Automatically resolve module imports like `import 'foundation-sites';`
// to their actual entry points using Node's resolution logic.
// This is necessary because the entryPoints (e.g., "../foundation_cms/static/js")
// live outside the directory that contains node_modules (/frontend/node_modules).

const aliasPlugin = {
  name: 'auto-alias-plugin',

  setup(build) {
    // Match module imports (e.g., 'foundation-sites', but not './file.js')
    build.onResolve({ filter: /^[^./].*/ }, (args) => {
      try {
        const resolvedPath = require.resolve(args.path, {
          paths: [__dirname], // Resolve relative to the esbuild.config.js location
        });
        return { path: resolvedPath };
      } catch (e) {
        // If the module can’t be resolved, allow ESBuild to handle it normally
        return;
      }
    });
  },
};

// We use a for...of loop instead of forEach because forEach doesn't handle async/await properly.
// forEach won't wait for the async function to finish before moving to the next item,
// which can cause unexpected behavior in sequential build tasks like this.
async function runBuilds() {
  for (const [name, config] of Object.entries(sources)) {
    const opts = {
      ...base,
      entryPoints: [path.join(inDir, "/", config.source)],
      outfile: path.join(outDir, `${name}.compiled.js`),
      bundle: config.bundle,
      plugins: [aliasPlugin],
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
