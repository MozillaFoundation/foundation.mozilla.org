let commonPlugins = [
  require('autoprefixer'),
];

let prodPlugins = [
  require('cssnano')({
    preset: ['default', {
        discardComments: {
            removeAll: true,
        },
        // 'cssnano' uses 'postcss-calc' module for calc() optimization.
        // 'postcss-calc' is currently having parsing issues with calc()
        // See https://github.com/postcss/postcss-calc/issues/77#issuecomment-491354918
        // Disabling opitimization for 'calc' in our config until the parsing bug is fixed
        calc: false
    }]
  })
];

module.exports = {
  plugins: process.env.NODE_ENV === 'production' ? commonPlugins.concat(prodPlugins) : commonPlugins
};
