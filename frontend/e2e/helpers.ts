import AxeBuilder from "@axe-core/playwright";
import { expect, type Locator, type Page } from "@playwright/test";
import { mkdir } from "node:fs/promises";
import { join } from "node:path";

export const visualDirectory = join(process.cwd(), "test-results", "rui16-visual");

export async function prepareVisualDirectory() {
  await mkdir(visualDirectory, { recursive: true });
}

export async function capture(page: Page, name: string, fullPage = true) {
  await page.screenshot({ path: join(visualDirectory, name), fullPage });
}

export async function switchToEnglish(page: Page) {
  if (await page.locator("html").getAttribute("lang") === "en") return;
  await page.getByRole("button", { name: /англійську/i }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
}

export async function switchToUkrainian(page: Page) {
  if (await page.locator("html").getAttribute("lang") === "uk") return;
  await page.getByRole("button", { name: /Ukrainian/i }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "uk");
}

export function resultNavigation(page: Page) {
  return page.getByRole("navigation", { name: "Research result sections" });
}

export async function navigate(page: Page, name: string) {
  await resultNavigation(page).getByRole("button", { name, exact: true }).click();
  await expect(page.getByRole("main").getByRole("heading", { level: 1, name, exact: true })).toBeVisible();
}

export async function focusByTab(page: Page, target: Locator, maximumTabs = 80) {
  await page.evaluate(() => (document.activeElement as HTMLElement | null)?.blur());
  for (let index = 0; index < maximumTabs; index += 1) {
    await page.keyboard.press("Tab");
    if (await target.evaluate((element) => element === document.activeElement)) return;
  }
  throw new Error(`Target was not keyboard reachable after ${maximumTabs} Tab presses.`);
}

export async function expectNoSeriousOrCriticalViolations(page: Page, label: string, exclude: string[] = []) {
  let scan = new AxeBuilder({ page });
  for (const selector of exclude) scan = scan.exclude(selector);
  const results = await scan.analyze();
  const blocking = results.violations.filter((violation) => violation.impact === "serious" || violation.impact === "critical");
  expect(blocking, `${label}: ${JSON.stringify(blocking, null, 2)}`).toEqual([]);
}

export function analyzeRequests(page: Page) {
  const requests: Array<Record<string, unknown>> = [];
  page.on("request", (request) => {
    if (request.method() !== "POST" || !request.url().endsWith("/api/v1/analyze")) return;
    requests.push(request.postDataJSON() as Record<string, unknown>);
  });
  return requests;
}
