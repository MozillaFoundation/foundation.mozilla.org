let propertiesToObject = require(`java.properties.js`).default;
let pug = require(`pug`);
let shelljs = require(`shelljs`);
let moment = require(`moment`);

// JSON includes

let pulseData = require(`../source/json/temp/pulse.json`);
let peopleData = require(`../source/json/temp/people.json`);
let upcomingData = require(`../source/json/upcoming.json`);
let newsData = require(`../source/json/news.json`);
let opportunityData = require(`../source/json/opportunities.json`);

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

buildPage(`home`, `/`, {pulse: pulseData});
buildPage(`people`, `/people`, peopleData);
buildPage(`support`, `/support`);
buildPage(`upcoming`, `/programs/upcoming`, upcomingData);
buildPage(`projects`, `/projects`, {pulse: pulseData});
buildPage(`about`, `/about`);
buildPage(`news`, `/news`, {news: newsData});
buildPage(`style-guide`, `/style-guide`);
buildPage(`join`, `/join`);

// Opportunities
// buildPage(`internet-health-report`, `/opportunity/internet-health-report`);
// buildPage(`fellowships`, `/opportunity/fellowships`);
// buildPage(`training`, `/opportunity/training`);

opportunityData.forEach((opportunity) => {
  buildPage(`opportunity`, `/opportunity/${opportunity.link.slug}`, opportunity);
});
