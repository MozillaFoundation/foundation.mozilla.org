const config = {
  workers: 2,
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    permissions: ["clipboard-read"],
  },
};

module.exports = config;
