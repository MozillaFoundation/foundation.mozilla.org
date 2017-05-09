// Echo out env that is deemed safe as public information (for use in healthcheck)

//
// NEVER EMIT PRIVATE KEYS OR OTHER SENSITIVE DATA!
//

let env = require(`../env.json`);

console.log(`\n`);
console.log(`PULSE_API_DOMAIN: ${env.PULSE_API_DOMAIN}`);
console.log(`PULSE_DOMAIN: ${env.PULSE_DOMAIN}`);
console.log(`NETWORK_API_DOMAIN: ${env.NETWORK_API_DOMAIN}`);
console.log(`VIRTUAL_ROOT: ${env.VIRTUAL_ROOT}`);
console.log(`TARGET_DOMAIN: ${env.TARGET_DOMAIN}`);
