'use strict';

let pug = require(`pug`);
let shelljs = require(`shelljs`);

let compiled = pug.renderFile(`source/index.pug`, {
  pretty: true
});

shelljs.ShellString(compiled).to(`dest/index.html`);
