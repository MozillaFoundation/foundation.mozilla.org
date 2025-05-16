import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

// __dirname replacement in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const entries = [
  // List of base .scss file names located in `inDir` (omit the .scss extension)
  "redesign_main",
  "pages/home_page",
];

const inDir = "../foundation_cms/static/scss";
const tempDir = "../foundation_cms/static/temp";
const outDir = "../foundation_cms/static/compiled/_css";

for (const entry of entries) {
  const input = path.resolve(__dirname, `${inDir}/${entry}.scss`);
  const tempOutput = path.resolve(__dirname, `${tempDir}/${entry}.unprocessed.css`);
  const finalOutput = path.resolve(__dirname, `${outDir}/${entry}.compiled.css`);

  try {
    // Compile SCSS to unprocessed CSS
    execSync(`sass ${input} ${tempOutput} --style=compressed`, { stdio: "inherit" });

    // Process with PostCSS
    execSync(
      `postcss ${tempOutput} -o ${finalOutput} --config ./postcss.config.js`,
      { stdio: "inherit" }
    );

    console.log(`Built CSS: ${entry}`);
  } catch (err) {
    console.error(`Failed to build CSS for ${entry}:`, err.message);
    process.exit(1);
  }
}
