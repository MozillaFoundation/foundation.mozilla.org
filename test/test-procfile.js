let fs = require(`fs`);
let path = require(`path`);
let lines = fs.readFileSync(path.join(__dirname,`..`,`Procfile`))
              .toString()
              .split(`\n`);

// A valid Procfile consists only of lines that start with
// "keyword: ...", where the keyword arguments cannot be spread
// over multiple lines, so we can test the start of every line
// for that {keyword, colon} presence:
let re = /^\w+:\s+/;
let passes = lines.every(l => (!l || l.match(re)));

// make sure to exit this script with the correct code:
process.exit(passes ? 0 : 1);
