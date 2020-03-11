let webpack = require(`webpack`);
let path = require(`path`);
let frontendPath = path.resolve(
  __dirname,
  `network-api`,
  `networkapi`,
  `frontend`,
  `_js`
);

let rules = [
  {
    test: /\.js(x?)$/,
    exclude: /node_modules/,
    loader: `babel-loader`,
    query: {
      presets: [
        [`@babel/preset-env`, { targets: `> 1%, last 2 versions` }],
        [`@babel/preset-react`]
      ]
    }
  }
];

let main = {
  devtool: false,
  entry: `./source/js/main.js`,
  output: {
    path: frontendPath,
    filename: `main.compiled.js`
  },
  module: {
    rules
  },
  plugins: [new webpack.EnvironmentPlugin(["NODE_ENV"])]
};

let bgMain = {
  devtool: false,
  entry: {
    "bg-main": `./source/js/buyers-guide/bg-main.js`,
    polyfills: `./source/js/polyfills.js`
  },
  output: {
    path: frontendPath,
    filename: `[name].compiled.js`
  },
  module: {
    rules
  }
};

let config = [main, bgMain];

module.exports = (env, argv) => {
  process.env.NODE_ENV = process.env.NODE_ENV || argv.mode;

  return config;
};
