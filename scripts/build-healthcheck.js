let env = require(`../env.json`);
let request = require(`request`);
let shell = require(`shelljs`);


// Echo latest commit

console.log(`<h2>Latest Commit</h2>`);

console.log(`<pre>`);
shell.exec(`git log -1 --no-color`);
console.log(`</pre>`);

// Echo out env that is deemed safe as public information (for use in healthcheck)

//
// NEVER EMIT PRIVATE KEYS OR OTHER SENSITIVE DATA!
//

console.log(`<h2>Environmental Variables</h2>`);

console.log(`<pre>`);
console.log(`PULSE_API_DOMAIN: ${env.PULSE_API_DOMAIN}`);
console.log(`PULSE_DOMAIN: ${env.PULSE_DOMAIN}`);
console.log(`NETWORK_API_DOMAIN: ${env.NETWORK_API_DOMAIN}`);
console.log(`VIRTUAL_ROOT: ${env.VIRTUAL_ROOT}`);
console.log(`TARGET_DOMAIN: ${env.TARGET_DOMAIN}`);
console.log(`</pre>`);

// Add links to changelog and upcoming commit list

let data;

request(env.JENKINS_API, (error, response, body) => {
  if (!error && response.statusCode === 200) {
    data = JSON.parse(body);

    let lastDeployedCommitHash = data.changeSet.items[0].commitId;
    let latestLocalCommitHash = shell.exec(`git rev-parse HEAD`, {silent: true}).toString().trim();

    console.log(`<h2>Change Sets</h2>`);

    console.log(`<ul>`);
    console.log(`<li><a href="https://github.com/mozilla/network/compare/${lastDeployedCommitHash}...${latestLocalCommitHash}">New commits since last deploy</a></li>`);
    console.log(`<li><a href="https://github.com/mozilla/network/compare/${latestLocalCommitHash}...master">Commits to master since this deploy (upcoming changes)</a></li>`);
    console.log(`</ul>`);
  } else {
    console.log(`Failed to pull Jenkins JSON`);
    shell.exit(1);
  }
});
