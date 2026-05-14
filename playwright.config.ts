import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 120_000,
  expect: { timeout: 15_000 },
  use: {
    baseURL: 'https://daily.powerbi.com',
    viewport: { width: 1600, height: 900 },
    // Slow down all actions so demo audience can follow
    launchOptions: {
      slowMo: 600,
    },
    // Keep browser open between tests in demo mode
    headless: false,
    screenshot: 'on',
    video: 'on',
    trace: 'on',
  },
  projects: [
    {
      name: 'demo-chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  reporter: [['html', { open: 'never' }], ['list']],
  outputDir: 'test-results',
});
