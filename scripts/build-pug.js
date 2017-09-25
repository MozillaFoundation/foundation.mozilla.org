let propertiesToObject = require(`java.properties.js`).default;
let pug = require(`pug`);
let shelljs = require(`shelljs`);
let moment = require(`moment`);

let environment = require(`../env.json`);

let rawStrings = shelljs.cat(`locales/en-US/general.properties`);

function buildPage(template, target, extraData, hasExternalTarget = false) {
  let viewData = {
    env: environment,
    strings: propertiesToObject(rawStrings.toString()),
    templateID: template,
    target: target,
    data: extraData,
    moment: moment
  };

  let fn = pug.compileFile(`source/pug/views/${template}.pug`, {
    pretty: true
  });

  let html = fn(viewData);

  if (!hasExternalTarget) {
    let path = `network-api/app/networkapi/frontend${target}`;

    shelljs.mkdir(`-p`, path);
    shelljs.ShellString(html).to(`${path}/index.html`);
  } else {
    shelljs.ShellString(html).to(target);
  }
}

buildPage(`home`, `/`);
buildPage(`people`, `/people`);
buildPage(`get-involved`, `/get-involved`);
buildPage(`upcoming`, `/programs/upcoming`);
buildPage(`projects`, `/projects`, require(`./massage-projects.js`));
buildPage(`about`, `/about`);
buildPage(`news`, `/news`, {news: JSON.parse((shelljs.cat(`source/json/temp/news.json`).toString()))});
buildPage(`style-guide`, `/style-guide`);
buildPage(`sign-up`, `/sign-up`);
buildPage(`404`, `/errors/404`);

// Opportunities Template – For Mezzanine (with tokens)
buildPage(`opportunity`, `network-api/app/networkapi/templates/pages/landingpage.html`, null, true);
