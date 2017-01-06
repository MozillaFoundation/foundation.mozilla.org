module.exports = {
  entry: `./source/js/main.js`,
  output: {
    filename: `./dest/_js/main.compiled.js`
  },
  module: {
    loaders: [
      {
        test: /\.js(x?)$/,
        exclude: /node_modules/,
        loader: `babel`,
        query: {
          presets: [`es2015`, `react`]
        }
      }
    ]
  }};
