import { context, build } from "esbuild";
import path from "path";
import { fileURLToPath } from "url";
import { createRequire } from 'module';
const require = createRequire(import.meta.url);


// __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Get build mode from CLI arg or env var
const arg = process.argv.indexOf("--node-env");
const mode =
  arg > 0 ? process.argv[arg + 1] : process.env.NODE_ENV || "development";
const inProduction = mode === "production";

console.log("ESBuild running in production mode?", inProduction);

const inDir = "../../foundation_cms/static/js";
const outDir = "../../foundation_cms/static/compiled/_js";

// JS entry points for ESBuild.
// `source` paths are relative to `inDir`. Output preserves directory structure.
const sources = {
  redesign_main: {
    source: "redesign_main.js",
    jsx: false,
    bundle: true,
  },
  home_page: {
    source: "pages/home_page.js",
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
// live outside the directory that contains node_modules (/frontend/redesign/node_modules).

const aliasPlugin = {
  name: 'auto-alias-plugin',

  setup(build) {
    build.onResolve({ filter: /^[^./].*/ }, (args) => {
      try {
        const resolvedPath = require.resolve(args.path);
        return { path: resolvedPath };
      } catch (e) {
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
    const sourcePath = path.join(inDir, config.source);
    const compiledFilename = config.source.replace(/\.js$/, ".compiled.js");
    const outputPath = path.join(outDir, compiledFilename);

    const opts = {
      ...base,
      entryPoints: [path.join(__dirname, sourcePath)],
      outfile: path.join(__dirname, outputPath),
      bundle: config.bundle,
      plugins: [aliasPlugin],
    };

    if (config.jsx) {
      opts.jsx = config.jsx;
    }

    if (inProduction) {
      await build(opts);
      console.log(`Built ${compiledFilename}`);
    } else {
      const ctx = await context(opts);
      await ctx.watch();
      console.log(`Watching ${compiledFilename}...`);
    }
  }
}

runBuilds().catch((err) => {
  console.error("Build failed:", err);
  process.exit(1);
});
