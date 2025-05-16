import { context, build } from "esbuild";
import path from "path";
import { fileURLToPath } from "url";

// __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Get build mode from CLI arg or env var
const arg = process.argv.indexOf("--node-env");
const mode =
  arg > 0 ? process.argv[arg + 1] : process.env.NODE_ENV || "development";
const inProduction = mode === "production";

console.log("ESBuild running in production mode?", inProduction);

const inDir = "../foundation_cms/static/js";
const outDir = "../foundation_cms/static/compiled/_js";

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
