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

fetchJSON(`pulse`, `https://network-pulse-api-production.herokuapp.com/entries/?ordering=-created&page_size=996&format=json&featured=True&page=1`);
fetchJSON(`people`, `https://network-api.mofoprod.net/people/?format=json&featured=True&page=1`);
fetchJSON(`news`, `https://network-api.mofoprod.net/news/?format=json&featured=True&page=1`);
