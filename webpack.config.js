let path = require('path');

let rules = [
  {
    test: /\.js(x?)$/,
    exclude: /node_modules/,
    loader: `babel-loader`,
    query: {
      presets: [`es2015`, `react`]
    }
  }
];

let main = {
  entry: `./source/js/main.js`,
  output: {
    path: path.resolve(__dirname, 'network-api','networkapi','frontend','_js'),
    filename: `main.compiled.js`
  },
  module: {
    rules
  }
};

let bgMain = {
  entry: `./source/js/buyers-guide/bg-main.js`,
  output: {
    path: path.resolve(__dirname, 'network-api','networkapi','frontend','_js'),
    filename: `bg-main.compiled.js`
  },
  module: {
    rules
  }
};

module.exports = [main, bgMain];
