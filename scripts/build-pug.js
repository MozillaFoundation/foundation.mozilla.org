'use strict';

let propertiesToObject = require(`java.properties.js`).default;
let pug = require(`pug`);
let shelljs = require(`shelljs`);

let rawStrings = shelljs.cat(`locales/en-US/general.properties`);

let localizedStrings = propertiesToObject(rawStrings.toString());

let fn = pug.compileFile(`source/index.pug`, {
  pretty: true
});

let html = fn(localizedStrings);

shelljs.ShellString(html).to(`dest/index.html`);
