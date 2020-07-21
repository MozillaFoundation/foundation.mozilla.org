let commonPlugins = [
  require('autoprefixer'),
];

let prodPlugins = [
  require('cssnano')({
    preset: ['default', {
        discardComments: {
            removeAll: true,
        },
    }]
  })
];

module.exports = {
  plugins: process.env.NODE_ENV !== 'production' ? commonPlugins.concat(prodPlugins) : commonPlugins
};