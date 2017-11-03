// Pull JSON from various web services

require(`dotenv`).config();

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

if (process.env.PULSE_API_DOMAIN) {
  fetchJSON(`pulse-privacy`, `https://${process.env.PULSE_API_DOMAIN}/api/pulse/entries/?issue=Online%20Privacy%20%26%20Security&featured=True&ordering=-created`);
  fetchJSON(`pulse-innovation`, `https://${process.env.PULSE_API_DOMAIN}/api/pulse/entries/?issue=Open%20Innovation&featured=True&ordering=-created`);
  fetchJSON(`pulse-inclusion`, `https://${process.env.PULSE_API_DOMAIN}/api/pulse/entries/?issue=Digital%20Inclusion&featured=True&ordering=-created`);
  fetchJSON(`pulse-decentralization`, `https://${process.env.PULSE_API_DOMAIN}/api/pulse/entries/?issue=Decentralization&featured=True&ordering=-created`);
  fetchJSON(`pulse-literacy`, `https://${process.env.PULSE_API_DOMAIN}/api/pulse/entries/?issue=Web%20Literacy&featured=True&ordering=-created`);
} else {
  console.error(chalk.red(`PULSE_API_DOMAIN is undefined!`));
  shell.exit(2);
}
