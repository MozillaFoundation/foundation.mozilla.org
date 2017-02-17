// Pull JSON from various web services

let request = require(`request`);
let shell = require(`shelljs`);
let chalk = require(`chalk`);

shell.mkdir(`-p`, `source/json/temp/`);

// Pulse
request(`https://network-pulse-api-production.herokuapp.com/entries/?ordering=-created&page_size=996&format=json&featured=True&page=1`, (error, response, body) => {
  if (!error && response.statusCode === 200) {
    console.log(chalk.green(`Pulled Pulse JSON`));
    shell.ShellString(body).to(`source/json/temp/pulse.json`);
  } else {
    console.log(chalk.red(`Failed to pull Pulse JSON!`));
    shell.exit(1);
  }
});
