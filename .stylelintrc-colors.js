  var config = {
    "plugins": ["stylelint-prettier"],
    "rules": {
      "color-named": "never",
      "color-no-hex": true,
      "declaration-property-value-disallowed-list": [
        {
          "/.*/": [
            /rgba{0,1}\(/i,
            /hsla{0,1}\(/i,
            /hwb\(/i,
            /gray\(/i
          ]
        },
        {
          "message": "Custom colors are not allowed. Please use brand colors listed in _colors.scss."
        }
      ]
    }
  };

  module.exports = config;
