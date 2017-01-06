let autoprefixer = require(`autoprefixer`);
let postcss = require(`postcss`);
let shelljs = require(`shelljs`);

let cssPath = `dest/css/main.compiled.css`;
let css = shelljs.cat(cssPath).toString();

postcss([ autoprefixer ]).process(css).then((result) => {
  result.warnings().forEach((warn) => {
    console.warn(warn.toString());
    shelljs.exit(1);
  });

  console.log(`Autoprefixed CSS: ${cssPath}`);
  shelljs.ShellString(result.css).to(cssPath);
  shelljs.exit(0);
});
