/** @type { import('@storybook/html-webpack5').StorybookConfig } */

const config = {
  stories: ["../stories/**/*.stories.js"],
  addons: [
    "@storybook/addon-webpack5-compiler-swc",
    "@storybook/addon-essentials",
    "@chromatic-com/storybook",
    "@storybook/addon-interactions",
  ],
  framework: {
    name: "@storybook/html-webpack5",
    options: {},
  },
  staticDirs: ["../foundation_cms/base/static"],
};
export default config;
