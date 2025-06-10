const config = {
  workers: 1,
  timeout: 60000, // 60 seconds per test
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    permissions: ["clipboard-read"],
    navigationTimeout: 60000, // 60 seconds for page.goto()
    actionTimeout: 60000, // 60 seconds for actions like clicks
  },
};

module.exports = config;
