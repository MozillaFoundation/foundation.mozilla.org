module.exports = {
  entry: `./source/js/main.js`,
  output: {
    filename: `./network-api/app/networkapi/frontend/_js/main.compiled.js`
  },
  module: {
    loaders: [
      {
        test: /\.js(x?)$/,
        exclude: /node_modules/,
        loader: `babel-loader`,
        query: {
          presets: [`es2015`, `react`]
        }
      }
    ]
  }};
