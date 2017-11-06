require(`dotenv`).config();

let request = require(`request`);
let shell = require(`shelljs`);

const Entities = require(`html-entities`).AllHtmlEntities;
const entities = new Entities();

console.log(`<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">`);
console.log(`<style type="text/css">body { max-width: 960px; margin: auto; padding: 40px 20px; } * { font-family: Helvetica, sans-serif; } pre { font-family: monospace; white-space: pre-wrap; }</style>`);
console.log(`<title>Network Status</title>`);

console.log(`<h1 class="mb-4"><a href="/">Network</a> Status</h1>`);

// Echo latest commit

console.log(`<h2 class="mb-3">Latest Deployed Commit</h2>`);

console.log(`<pre class="mb-4">`);
console.log(entities.encode(shell.exec(`git log -1 --no-color`, {silent: true}).stdout.trim()));
console.log(`</pre>`);

// Echo out env that is deemed safe as public information (for use in healthcheck)

//              _,.-------.,_
//          ,;~'             '~;,
//        ,;                     ;,
//       ;                         ;
//      ,'                         ',
//    ,;                           ;,
//    ; ;      .           .      ; ;
//    | ;   ______       ______   ; |
//    |  `/~"     ~" . "~     "~\'  |
//    |  ~  ,-~~~^~, | ,~^~~~-,  ~  |
//     |   |        }:{        |   |
//     |   l       / | \       !   |
//     .~  (__,.--" .^. "--.,__)  ~.
//     |     ---;' / | \ `;---     |
//      \__.       \/^\/       .__/
//       V| \                 / |V
//        | |T~\___!___!___/~T| |
//        | |`IIII_I_I_I_IIII'| |
//        |  \,III I I I III,/  |
//         \   `~~~~~~~~~~'    /
//           \   .       .   /
//             \.    ^    ./
//               ^~~~^~~~^
//
//     NEVER EMIT PRIVATE KEYS OR OTHER SENSITIVE DATA!
//

console.log(`<h2 class="mb-3">Environmental Variables</h2>`);

console.log(`<pre class="mb-4">`);
console.log(`PULSE_API_DOMAIN: ${process.env.PULSE_API_DOMAIN}`);
console.log(`PULSE_DOMAIN: ${process.env.PULSE_DOMAIN}`);
console.log(`NETWORK_API_DOMAIN: ${process.env.NETWORK_API_DOMAIN}`);
console.log(`TARGET_DOMAIN: ${process.env.TARGET_DOMAIN}`);
console.log(`</pre>`);

// Add links to changelog and upcoming commit list

let data;

request(process.env.JENKINS_API, (error, response, body) => {
  if (!error && response.statusCode === 200) {
    data = JSON.parse(body);

    let lastDeployedCommitHash = data.commitId;
    let latestLocalCommitHash = shell.exec(`git rev-parse HEAD`, {silent: true}).toString().trim();

    console.log(`<h2 class="mb-3">Change Sets</h2>`);

    console.log(`<ul>`);
    console.log(`<li><a href="https://github.com/mozilla/network/compare/${lastDeployedCommitHash}...${latestLocalCommitHash}"><strong>Changelog</strong></a></li>`);
    console.log(`<li><a href="https://github.com/mozilla/network/compare/${latestLocalCommitHash}...master"><strong>Upcoming Changes</strong></a></li>`);
    console.log(`</ul>`);
  } else {
    console.log(`Failed to pull Jenkins JSON`);
    shell.exit(1);
  }
});
