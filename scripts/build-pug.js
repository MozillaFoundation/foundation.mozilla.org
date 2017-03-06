let propertiesToObject = require(`java.properties.js`).default;
let pug = require(`pug`);
let shelljs = require(`shelljs`);

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
    data: extraData
  };

  let fn = pug.compileFile(`source/pug/views/${template}.pug`, {
    pretty: true
  });

  let html = fn(viewData);
  let path = `dest${target}`;

  shelljs.mkdir(`-p`, path);
  shelljs.ShellString(html).to(`${path}/index.html`);
}

buildPage(`home`, `/`, {pulse: JSON.parse((shelljs.cat(`source/json/temp/pulse.json`).toString()))});
buildPage(`people`, `/people`, JSON.parse((shelljs.cat(`source/json/people.json`).toString())));
buildPage(`programs`, `/programs`);
buildPage(`upcoming`, `/programs/upcoming`);
buildPage(`fellowships`, `/programs/fellowships`);
buildPage(`free-leadership-training`, `/programs/free-leadership-training`);
buildPage(`projects`, `/projects`, {pulse: JSON.parse((shelljs.cat(`source/json/temp/pulse.json`).toString()))});
buildPage(`about`, `/about`);
buildPage(`news`, `/news`);
buildPage(`style-guide`, `/style-guide`);

// Landing Pages:
buildPage(`internet-health-report`, `/landing/internet-health-report`);
