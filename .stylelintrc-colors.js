  var config = {
    "plugins": ["stylelint-prettier"],
    "rules": {
      "color-no-hex": true,
      "declaration-property-value-blacklist": [
        {
          "/.*/": [
            /rgba{0,1}\(/i,
            /hsla{0,1}\(/i,
            /hwb\(/i,
            /gray\(/i,
            // uses of web color names are not allowed (with 'white' and 'black' being the only exceptions)
            /[^\$-\w](lavender|thistle|plum|violet|orchid|fuchsia|magenta|mediumorchid|mediumpurple|blueviolet|darkviolet|darkorchid|darkmagenta|purple|indigo|darkslateblue|slateblue|mediumslateblue|pink|lightpink|hotpink|deeppink|palevioletred|mediumvioletred|lightsalmon|salmon|darksalmon|lightcoral|indianred|crimson|firebrick|darkred|red|orangered|tomato|coral|darkorange|orange|yellow|lightyellow|lemonchiffon|lightgoldenrodyellow|papayawhip|moccasin|peachpuff|palegoldenrod|khaki|darkkhaki|gold|cornsilk|blanchedalmond|bisque|navajowhite|wheat|burlywood|tan|rosybrown|sandybrown|goldenrod|darkgoldenrod|per|chocolate|saddlebrown|sienna|brown|maroon|darkolivegreen|olive|olivedrab|yellowgreen|limegreen|lime|lawngreen|chartreuse|greenyellow|springgreen|mediumspringgreen|lightgreen|palegreen|darkseagreen|mediumseagreen|seagreen|forestgreen|green|darkgreen|mediumaquamarine|aqua|cyan|lightcyan|paleturquoise|aquamarine|turquoise|mediumturquoise|darkturquoise|lightseagreen|cadetblue|darkcyan|teal|lightsteelblue|powderblue|lightblue|skyblue|lightskyblue|deepskyblue|dodgerblue|cornflowerblue|steelblue|royalblue|blue|mediumblue|darkblue|navy|midnightblue|snow|honeydew|mintcream|azure|aliceblue|ghostwhite|whitesmoke|seashell|beige|oldlace|floralwhite|ivory|antiquewhite|linen|lavenderblush|mistyrose|gainsboro|lightgray|silver|darkgray|gray|dimgray|lightslategray|slategray|darkslategray)/i,
            /^(lavender|thistle|plum|violet|orchid|fuchsia|magenta|mediumorchid|mediumpurple|blueviolet|darkviolet|darkorchid|darkmagenta|purple|indigo|darkslateblue|slateblue|mediumslateblue|pink|lightpink|hotpink|deeppink|palevioletred|mediumvioletred|lightsalmon|salmon|darksalmon|lightcoral|indianred|crimson|firebrick|darkred|red|orangered|tomato|coral|darkorange|orange|yellow|lightyellow|lemonchiffon|lightgoldenrodyellow|papayawhip|moccasin|peachpuff|palegoldenrod|khaki|darkkhaki|gold|cornsilk|blanchedalmond|bisque|navajowhite|wheat|burlywood|tan|rosybrown|sandybrown|goldenrod|darkgoldenrod|per|chocolate|saddlebrown|sienna|brown|maroon|darkolivegreen|olive|olivedrab|yellowgreen|limegreen|lime|lawngreen|chartreuse|greenyellow|springgreen|mediumspringgreen|lightgreen|palegreen|darkseagreen|mediumseagreen|seagreen|forestgreen|green|darkgreen|mediumaquamarine|aqua|cyan|lightcyan|paleturquoise|aquamarine|turquoise|mediumturquoise|darkturquoise|lightseagreen|cadetblue|darkcyan|teal|lightsteelblue|powderblue|lightblue|skyblue|lightskyblue|deepskyblue|dodgerblue|cornflowerblue|steelblue|royalblue|blue|mediumblue|darkblue|navy|midnightblue|snow|honeydew|mintcream|azure|aliceblue|ghostwhite|whitesmoke|seashell|beige|oldlace|floralwhite|ivory|antiquewhite|linen|lavenderblush|mistyrose|gainsboro|lightgray|silver|darkgray|gray|dimgray|lightslategray|slategray|darkslategray)/i
          ]
        },
        {
          "message": "Custom colors are not allowed. Please use brand colors listed in _colors.scss."
        }
      ]
    }
  };

  module.exports = config;
