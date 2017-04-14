// Pull JSON from various web services

let request = require(`request`);
let shell = require(`shelljs`);
let chalk = require(`chalk`);

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

fetchJSON(`pulse-homepage`, `https://network-pulse-api-production.herokuapp.com/entries/216`);
fetchJSON(`pulse-privacy`, `https://network-pulse-api-production.herokuapp.com/entries/?issue=Online%20Privacy%20%26%20Security&featured=True&page_size=2`);
fetchJSON(`pulse-mozfest`, `https://network-pulse-api-production.herokuapp.com/entries/?tag=mozfest&featured=True&page_size=2`);
fetchJSON(`pulse-innovation`, `https://network-pulse-api-production.herokuapp.com/entries/?issue=Open%20Innovation&featured=True&page_size=2`);
fetchJSON(`pulse-games`, `https://network-pulse-api-production.herokuapp.com/entries/?tag=game&featured=True&page_size=2`);
fetchJSON(`people`, `https://network-api.mofoprod.net/api/people/?format=json&featured=True&page=1`);
fetchJSON(`news`, `https://network-api.mofoprod.net/api/news/?format=json&featured=True&page=1`);
