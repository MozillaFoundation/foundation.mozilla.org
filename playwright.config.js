const config = {
  workers: 1,
  timeout: 90000,
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    permissions: ["clipboard-read"],
    navigationTimeout: 90000,
    trace: "on",
  },
};

module.exports = config;
