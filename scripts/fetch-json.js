// Pull JSON from various web services

let request = require(`request`);
let shell = require(`shelljs`);
let chalk = require(`chalk`);

let pulseApiDomain = `network-pulse-api-production.herokuapp.com`;
let networkApiDomain = `network.mofoprod.net`;

if (process.env.PULSE_API_DOMAIN) {
  pulseApiDomain = process.env.PULSE_API_DOMAIN;
}

if (process.env.NETWORK_API_DOMAIN) {
  networkApiDomain = process.env.NETWORK_API_DOMAIN;
}

shell.mkdir(`-p`, `source/json/temp/`);

let fetchJSON = (shortName, source) => {
  request(source, (error, response, body) => {
    if (!error && response.statusCode === 200) {
      console.log(chalk.green(`Pulled ${shortName} JSON`));
      shell.ShellString(body).to(`source/json/temp/${shortName}.json`);
    } else {
      console.log(chalk.red(`Failed to pull ${shortName} JSON!`));
      shell.exit(1);
    }
  });
};

fetchJSON(`pulse-homepage`, `https://${pulseApiDomain}/entries/216`);
fetchJSON(`pulse-privacy`, `https://${pulseApiDomain}/entries/?issue=Online%20Privacy%20%26%20Security&featured=True&page_size=2`);
fetchJSON(`pulse-mozfest`, `https://${pulseApiDomain}/entries/?tag=mozfest&featured=True&page_size=2`);
fetchJSON(`pulse-innovation`, `https://${pulseApiDomain}/entries/?issue=Open%20Innovation&featured=True&page_size=2`);
fetchJSON(`pulse-games`, `https://${pulseApiDomain}/entries/?tag=game&featured=True&page_size=2`);
fetchJSON(`people`, `https://${networkApiDomain}/api/people/?format=json&featured=True&page=1`);
fetchJSON(`news`, `https://${networkApiDomain}/api/news/?format=json&featured=True&page=1`);
