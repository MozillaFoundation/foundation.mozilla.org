const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const entries = ["redesign_main"];

const inDir = "../foundation_cms/static/scss";
const tempDir = "../foundation_cms/static/temp";
const outDir = "../foundation_cms/static/compiled/_css";

entries.forEach((entry) => {
  const input = path.resolve(__dirname, `${inDir}/${entry}.scss`);
  const tempOutput = path.resolve(
    __dirname,
    `${tempDir}/${entry}.unprocessed.css`
  );
  const finalOutput = path.resolve(
    __dirname,
    `${outDir}/${entry}.compiled.css`
  );

  try {
    // Compile SCSS to unprocessed CSS
    execSync(`sass ${input} ${tempOutput} --style=compressed`, {
      stdio: "inherit",
    });

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
});
