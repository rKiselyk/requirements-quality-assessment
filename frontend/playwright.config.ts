import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig, devices } from "@playwright/test";

const repositoryRoot = fileURLToPath(new URL("..", import.meta.url));
const virtualEnvironmentPython = process.platform === "win32"
  ? resolve(repositoryRoot, ".venv", "Scripts", "python.exe")
  : resolve(repositoryRoot, ".venv", "bin", "python");
const python = existsSync(virtualEnvironmentPython)
  ? `"${virtualEnvironmentPython}"`
  : "python";
const localBrowserChannel = process.env.RUI16_BROWSER_CHANNEL as "chrome" | "msedge" | undefined;
const acceptanceApiUrl = "http://127.0.0.1:8126";
const acceptanceWebUrl = "http://127.0.0.1:5176";

export default defineConfig({
  testDir: "./e2e",
  outputDir: "./test-results/playwright",
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 2 : 0,
  reporter: [["list"], ["html", { outputFolder: "playwright-report", open: "never" }]],
  use: {
    baseURL: acceptanceWebUrl,
    viewport: { width: 1440, height: 1000 },
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "off",
  },
  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        ...(localBrowserChannel ? { channel: localBrowserChannel } : {}),
      },
    },
  ],
  webServer: [
    {
      command: `${python} -m uvicorn requirements_quality_assessment.api.app:app --host 127.0.0.1 --port 8126`,
      cwd: repositoryRoot,
      url: `${acceptanceApiUrl}/health`,
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: "npm run dev -- --host 127.0.0.1 --port 5176",
      env: { RQA_API_TARGET: acceptanceApiUrl },
      url: acceptanceWebUrl,
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
