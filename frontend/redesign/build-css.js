import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

// __dirname replacement in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const entries = [
  // List of base .scss file names located in `inDir` (omit the .scss extension)
  "redesign_fallback",
  "redesign_migrated_content",
  "pages/campaign_page",
  "pages/home_page",
  "pages/topic_listing_page",
  "pages/nothing_personal/article_page",
  "pages/nothing_personal/podcast_page",
  "pages/nothing_personal/product_collection_page",
  "pages/nothing_personal/product_review_page",
  "pages/nothing_personal/home_page",
];

const inDir = "../../foundation_cms/static/scss";
const tempDir = "../../foundation_cms/static/temp";
const outDir = "../../foundation_cms/static/compiled/_css";

const isDev = process.env.NODE_ENV !== "production";

for (const entry of entries) {
  const input = path.resolve(__dirname, `${inDir}/${entry}.scss`);
  const tempOutput = path.resolve(
    __dirname,
    `${tempDir}/${entry}.unprocessed.css`,
  );
  const finalOutput = path.resolve(
    __dirname,
    `${outDir}/${entry}.compiled.css`,
  );

  try {
    // Compile SCSS to unprocessed CSS with source maps in dev
    const sassCmd = isDev
      ? `sass ${input} ${tempOutput} --source-map --quiet`
      : `sass ${input} ${tempOutput} --style=compressed --quiet`;

    execSync(sassCmd, { stdio: "inherit" });

    // Process with PostCSS, preserving source maps in dev
    const postcssCmd = isDev
      ? `postcss ${tempOutput} -o ${finalOutput} --config ./postcss.config.js --map`
      : `postcss ${tempOutput} -o ${finalOutput} --config ./postcss.config.js`;

    execSync(postcssCmd, { stdio: "inherit" });

    console.log(`Built CSS: ${entry}`);
  } catch (err) {
    console.error(`Failed to build CSS for ${entry}:`, err.message);
    process.exit(1);
  }
}
