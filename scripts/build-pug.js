'use strict';

let propertiesToObject = require(`java.properties.js`).default;
let pug = require(`pug`);
let shelljs = require(`shelljs`);

let rawStrings = shelljs.cat(`locales/en-US/general.properties`);

let localizedStrings = {
  strings: propertiesToObject(rawStrings.toString())
};

function buildPage(template, target) {
  let fn = pug.compileFile(`source/pug/views/${template}.pug`, {
    pretty: true
  });

  let html = fn(localizedStrings);
  let path = `dest/${target}`;

  shelljs.mkdir(`-p`, path);
  shelljs.ShellString(html).to(`${path}/index.html`);
}

buildPage(`home`, ``);
buildPage(`subpage1`, `subpage1`);
buildPage(`subpage2`, `subpage2`);
