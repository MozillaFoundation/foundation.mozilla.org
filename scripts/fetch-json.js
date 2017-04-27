// Pull JSON from various web services

let request = require(`request`);
let shell = require(`shelljs`);
let chalk = require(`chalk`);

let environment = require(`../env.json`);

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

fetchJSON(`pulse-homepage`, `https://${environment[`PULSE_API_DOMAIN`]}/entries/216`);
fetchJSON(`pulse-privacy`, `https://${environment[`PULSE_API_DOMAIN`]}/entries/?issue=Online%20Privacy%20%26%20Security&featured=True&page_size=2`);
fetchJSON(`pulse-mozfest`, `https://${environment[`PULSE_API_DOMAIN`]}/entries/?tag=mozfest&featured=True&page_size=2`);
fetchJSON(`pulse-innovation`, `https://${environment[`PULSE_API_DOMAIN`]}/entries/?issue=Open%20Innovation&featured=True&page_size=2`);
fetchJSON(`pulse-games`, `https://${environment[`PULSE_API_DOMAIN`]}/entries/?tag=game&featured=True&page_size=2`);
fetchJSON(`people`, `https://${environment[`NETWORK_API_DOMAIN`]}/api/people/?format=json&featured=True&page=1`);
fetchJSON(`news`, `https://${environment[`NETWORK_API_DOMAIN`]}/api/news/?format=json&featured=True&page=1`);
