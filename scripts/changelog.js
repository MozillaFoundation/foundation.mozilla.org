let env = require(`../env.json`);
let request = require(`request`);
let shell = require(`shelljs`);

let data;

request(env.JENKINS_API, (error, response, body) => {
  if (!error && response.statusCode === 200) {
    data = JSON.parse(body);

    let latestDeployedCommmitHash = data.changeSet.items[0].commitId;
    let latestLocalCommitHash = shell.exec(`git rev-parse HEAD`, {silent: true});

    console.log(`\nChangelog:\n`);
    console.log(`https://github.com/mozilla/network/compare/${latestDeployedCommmitHash}...${latestLocalCommitHash.toString()}`);

    console.log(`\nCommits since this deploy:\n`);
    console.log(`https://github.com/mozilla/network/compare/${latestDeployedCommmitHash.toString()}...master`);

    shell.exit(0);
  } else {
    console.log(`Failed to pull Jenkins JSON`);
    shell.exit(1);
  }
});
