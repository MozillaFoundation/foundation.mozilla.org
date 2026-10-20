import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  timeout: 60000,
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    navigationTimeout: 60000,
    actionTimeout: 60000,
  },
  webServer: {
    url: "http://localhost:8000/en/",
    reuseExistingServer: true,
    timeout: 30000,
  },
});
