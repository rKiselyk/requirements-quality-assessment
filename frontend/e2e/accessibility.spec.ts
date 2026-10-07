import { expect, test } from "@playwright/test";
import {
  expectNoSeriousOrCriticalViolations,
  navigate,
  switchToEnglish,
} from "./helpers";

const requirement = "Система повинна швидко оновити статус.";

test.describe.configure({ timeout: 900_000 });

test("accessibility smoke covers input, INITIAL, and controlled lifecycle pages", async ({ page }) => {
  await page.goto("/");
  await switchToEnglish(page);
  await expectNoSeriousOrCriticalViolations(page, "input page");

  await page.getByRole("textbox", { name: "Paste or edit requirements" }).fill(requirement);
  await page.getByRole("button", { name: "Analyze", exact: true }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Overview" })).toBeVisible({ timeout: 300_000 });
  await expectNoSeriousOrCriticalViolations(page, "INITIAL Overview");
  await navigate(page, "Requirements");
  await expectNoSeriousOrCriticalViolations(page, "INITIAL Requirements");

  await page.getByRole("button", { name: "New specification" }).click();
  await page.getByRole("button", { name: "Load demonstration example" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Overview" })).toBeVisible({ timeout: 600_000 });
  await expectNoSeriousOrCriticalViolations(page, "controlled-demo Overview");
  for (const section of ["Process", "Audit", "Reassessment", "Comparison"]) {
    await navigate(page, section);
    await expectNoSeriousOrCriticalViolations(
      page,
      `controlled-demo ${section}`,
      section === "Audit" ? [".audit-node__children"] : [],
    );
  }
});
