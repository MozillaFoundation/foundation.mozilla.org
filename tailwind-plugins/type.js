const plugin = require("tailwindcss/plugin");

module.exports = [
  plugin(function ({ addBase, addComponents, theme }) {
    const media = (breakpoint) => `@media (min-width: ${breakpoint})`;
    const rules = [
      {
        base: "a",
        styles: (componentType) => ({
          color: theme("colors.blue.dark"),
          "&:hover,&:focus,&:active": {
            color: theme("colors.blue.dark"),
            textDecoration: "underline",
          },
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            fontWeight: "inherit",
            "&:hover,&:focus,&:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
            '&[class*="btn"]': {
              fontWeight: theme("fontWeight.bold"),
              "&:hover,&:focus,&:active": {
                textDecoration: "none",
              },
            },
          },
          '&[class*="btn"]': {
            fontWeight: theme("fontWeight.bold"),
            "&:hover,&:focus,&:active": {
              textDecoration: "none",
            },
          },
        }),
      },
      {
        base: "h1",
        class: ".h1-heading",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.normal"),
          marginBottom: theme("spacing.4"),
          color: theme("colors.black"),
          lineHeight: 1.2,
          fontFamily: theme("fontFamily.zilla"),
          fontSize: theme("fontSize.4xl"),
          letterSpacing: theme("letterSpacing.normal"),
          [media(theme("screens.medium"))]: {
            fontSize: "48px",
          },
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
          a: {
            color: "inherit",
            fontWeight: "inherit",
            "&:hover,&:focus,&:active": {
              color: "inherit",
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        base: "h2",
        class: ".h2-heading",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.light"),
          marginBottom: theme("spacing.4"),
          color: theme("colors.black"),
          lineHeight: 1.2,
          fontFamily: theme("fontFamily.zilla"),
          fontSize: "28px",
          letterSpacing: theme("letterSpacing.normal"),
          [media(theme("screens.medium"))]: {
            fontSize: "40px",
          },
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
          a: {
            color: "inherit",
            fontWeight: "inherit",
            "&:hover,&:focus,&:active": {
              color: "inherit",
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        base: "h3",
        class: ".h3-heading",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.normal"),
          marginBottom: theme("spacing.4"),
          color: theme("colors.black"),
          lineHeight: 1.2,
          fontFamily: theme("fontFamily.zilla"),
          fontSize: "24px",
          letterSpacing: theme("letterSpacing.normal"),
          [media(theme("screens.medium"))]: {
            fontSize: "28px",
          },
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
          a: {
            color: "inherit",
            fontWeight: "inherit",
            "&:hover,&:focus,&:active": {
              color: "inherit",
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        base: "h4",
        class: ".h4-heading",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.normal"),
          marginBottom: theme("spacing.4"),
          color: theme("colors.black"),
          lineHeight: 1.3,
          fontFamily: theme("fontFamily.zilla"),
          fontSize: "22px",
          letterSpacing: theme("letterSpacing.normal"),
          [media(theme("screens.medium"))]: {
            fontSize: "24px",
          },
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
          a: {
            color: "inherit",
            fontWeight: "inherit",
            "&:hover,&:focus,&:active": {
              color: "inherit",
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        base: "h5",
        class: ".h5-heading",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.semibold"),
          marginBottom: theme("spacing.4"),
          color: theme("colors.black"),
          lineHeight: 1.3,
          fontFamily: theme("fontFamily.zilla"),
          fontSize: "20px",
          letterSpacing: theme("letterSpacing.normal"),
          [media(theme("screens.medium"))]: {
            fontSize: "22px",
          },
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
          a: {
            color: "inherit",
            fontWeight: "inherit",
            "&:hover,&:focus,&:active": {
              color: "inherit",
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        base: "h6",
        class: ".h6-heading",
        styles: (componentType) => ({
          textTransform: "uppercase",
          fontWeight: theme("fontWeight.normal"),
          marginBottom: theme("spacing.4"),
          color: theme("colors.gray.60"),
          lineHeight: 1.3,
          letterSpacing: theme("letterSpacing.wide"),
          fontFamily: theme("fontFamily.sans"),
          fontSize: "12px",
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
            },
          },
          a: {
            color: "inherit",
            fontWeight: "inherit",
            "&:hover,&:focus,&:active": {
              color: "inherit",
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        class: ".quote",
        styles: (componentType) => ({
          fontStyle: "italic",
          fontWeight: theme("fontWeight.light"),
          color: theme("colors.black"),
          lineHeight: 1.3,
          fontFamily: theme("fontFamily.zilla"),
          fontSize: "24px",
          [media(theme("screens.medium"))]: {
            fontSize: "30px",
          },
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            a: {
              color: theme("colors.blue.light"),
            },
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        class: ".type-accent",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.normal"),
          color: theme("colors.gray.20"),
          lineHeight: 1.2,
          fontFamily: theme("fontFamily.zilla"),
          fontSize: "56px",
          [media(theme("screens.medium"))]: {
            fontSize: "72px",
          },
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.gray.20"),
            a: {
              color: theme("colors.blue.light"),
            },
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        class: ".body-large,.body-large p",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.light"),
          color: theme("colors.black"),
          lineHeight: 1.3,
          fontFamily: theme("fontFamily.sans"),
          fontSize: "18px",
          [media(theme("screens.medium"))]: {
            fontSize: "20px",
          },
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            a: {
              color: theme("colors.blue.light"),
            },
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        base: "ul,ol,p",
        class: ".body",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.normal"),
          color: theme("colors.black"),
          lineHeight: 1.5,
          fontFamily: theme("fontFamily.sans"),
          fontSize: "18px",
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.white"),
            a: {
              color: theme("colors.blue.light"),
            },
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        class: ".body-small",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.normal"),
          color: theme("colors.gray.60"),
          lineHeight: 1.3,
          fontFamily: theme("fontFamily.sans"),
          fontSize: "12px",
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.gray.40"),
            a: {
              color: theme("colors.blue.light"),
            },
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
        }),
      },
      {
        class: ".cta-link",
        styles: (componentType) => ({
          fontWeight: theme("fontWeight.bold"),
          lineHeight: 1.5,
          display: "inline-block",
          fontSize: "18px",
          [componentType ? ".dark &" : ".tw-dark &"]: {
            color: theme("colors.blue.light"),
            a: {
              color: theme("colors.blue.light"),
            },
            "& a:hover,& a:focus,& a:active": {
              color: theme("colors.blue.light"),
              textDecoration: "underline",
            },
          },
          "&::after": {
            content: '" →"',
            textDecoration: "none",
            display: "inline-block",
            marginLeft: "0.333em",
            position: "relative",
            top: "-1px",
          },
        }),
      },
    ];

    let [bases, components] = [{}, {}];
    for (const rule of rules) {
      if (rule.base) {
        // we need to add a toggle because bases do not add prefixes to the selectors mentioned
        bases[rule.base] = rule.styles(false);
      }
      if (rule.class) {
        components[rule.class] = rule.styles(true);
      }
    }

    addComponents([components]);
    addBase([bases]);
  }),
];
