/** @type { import('@storybook/html-webpack5').Preview } */

import "../foundation_cms/base/static/css/design_system_test.css";

const preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
