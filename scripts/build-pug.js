'use strict';

let propertiesToObject = require(`java.properties.js`).default;
let pug = require(`pug`);
let shelljs = require(`shelljs`);

let rawStrings = shelljs.cat(`locales/en-US/general.properties`);

function buildPage(template, target) {
  let viewData = {
    strings: propertiesToObject(rawStrings.toString()),
    templateID: template
  };

  let fn = pug.compileFile(`source/pug/views/${template}.pug`, {
    pretty: true
  });

  let html = fn(viewData);
  let path = `dest${target}`;

  shelljs.mkdir(`-p`, path);
  shelljs.ShellString(html).to(`${path}/index.html`);
}

buildPage(`home`, `/`);
buildPage(`subpage1`, `/subpage1`);
buildPage(`subpage2`, `/subpage2`);
