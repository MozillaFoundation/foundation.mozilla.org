let propertiesToObject = require(`java.properties.js`).default;
let pug = require(`pug`);
let shelljs = require(`shelljs`);
let moment = require(`moment`);

let envFlag = process.argv[2];
let environmentVariables;

if (envFlag && envFlag === `--staging`) {
  environmentVariables = JSON.parse((shelljs.cat(`env/staging.json`).toString()));
} else {
  environmentVariables = JSON.parse((shelljs.cat(`env/default.json`).toString()));
}

let rawStrings = shelljs.cat(`locales/en-US/general.properties`);

function buildPage(template, target, extraData) {
  let viewData = {
    env: environmentVariables,
    strings: propertiesToObject(rawStrings.toString()),
    templateID: template,
    data: extraData,
    moment: moment
  };

  let fn = pug.compileFile(`source/pug/views/${template}.pug`, {
    pretty: true
  });

  let html = fn(viewData);
  let path = `dest${target}`;

  shelljs.mkdir(`-p`, path);
  shelljs.ShellString(html).to(`${path}/index.html`);
}

buildPage(`home`, `/`, {news: JSON.parse((shelljs.cat(`source/json/temp/news.json`).toString()))});
buildPage(`people`, `/people`, JSON.parse((shelljs.cat(`source/json/temp/people.json`).toString())));
buildPage(`support`, `/support`);
buildPage(`upcoming`, `/programs/upcoming`, JSON.parse((shelljs.cat(`source/json/upcoming.json`).toString())));
buildPage(`projects`, `/projects`, {pulse: JSON.parse((shelljs.cat(`source/json/temp/pulse.json`).toString()))});
buildPage(`about`, `/about`);
buildPage(`news`, `/news`, {news: JSON.parse((shelljs.cat(`source/json/temp/news.json`).toString()))});
buildPage(`style-guide`, `/style-guide`);
buildPage(`sign-up`, `/sign-up`);

// Opportunities
buildPage(`internet-health-report`, `/opportunity/internet-health-report`);
buildPage(`fellowships`, `/opportunity/fellowships`);
buildPage(`training`, `/opportunity/training`);
