let loaders = [
  {
    test: /\.js(x?)$/,
    exclude: /node_modules/,
    loader: `babel-loader`,
    query: {
      presets: [`es2015`, `react`]
    }
  }
];

module.exports = [{
  entry: `./source/js/main.js`,
  output: {
    filename: `./network-api/networkapi/frontend/_js/main.compiled.js`
  },
  module: {
    loaders: loaders
  }
}, {
  entry: `./source/js/buyers-guide/bg-main.js`,
  output: {
    filename: `./network-api/networkapi/frontend/_js/bg-main.compiled.js`
  },
  module: {
    loaders: loaders
  }
}];
