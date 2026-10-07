import { expect, test } from "@playwright/test";
import {
  analyzeRequests,
  capture,
  focusByTab,
  navigate,
  prepareVisualDirectory,
  resultNavigation,
  switchToEnglish,
  switchToUkrainian,
} from "./helpers";

const completeRequirement = "Якщо сервіс недоступний, система повинна відповісти не більше ніж за 2 с.";
const vagueRequirement = "Система повинна швидко оновити статус.";
const baseSections = [
  "Overview",
  "Requirements",
  "Specification",
  "Product Quality",
  "Risk",
  "Corrective Actions",
  "Process",
  "Audit",
];

test.describe.configure({ timeout: 600_000 });

test.beforeAll(async () => {
  await prepareVisualDirectory();
});

test("Research UI v1 integrated Scenario A, B, C, localization, keyboard, and responsive acceptance", async ({ page }) => {
  const requests = analyzeRequests(page);

  // Scenario A — one ordinary INITIAL request and the eight-page result surface.
  await page.goto("/");
  await switchToEnglish(page);
  const editor = page.getByRole("textbox", { name: "Paste or edit requirements" });
  const analyze = page.getByRole("button", { name: "Analyze", exact: true });
  await expect(analyze).toBeDisabled();
  await expect(page.getByText("Enter at least one non-empty requirement.")).toBeVisible();
  await editor.fill(`${completeRequirement}\n\n${vagueRequirement}`);
  await expect(page.getByText("Parsed requirements: 2")).toBeVisible();
  await focusByTab(page, analyze);
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main").getByRole("heading", { level: 1, name: "Overview" })).toBeVisible({ timeout: 300_000 });

  expect(requests).toHaveLength(1);
  expect(requests[0]).toEqual({
    case: "INITIAL",
    requirements: [
      { text: completeRequirement, source_line: 1 },
      { text: vagueRequirement, source_line: 3 },
    ],
  });
  await expect(resultNavigation(page).getByRole("button")).toHaveText(baseSections);
  await expect(resultNavigation(page).getByRole("button", { name: "Reassessment" })).toHaveCount(0);
  await expect(resultNavigation(page).getByRole("button", { name: "Comparison" })).toHaveCount(0);
  await expect(page.getByText("INITIAL", { exact: true })).toBeVisible();
  await capture(page, "a1-initial-overview.png");

  await navigate(page, "Requirements");
  const requirementsPage = page.locator(".requirements-page");
  await expect(requirementsPage.getByText(completeRequirement, { exact: true }).first()).toBeVisible();
  await page.getByRole("navigation", { name: "Canonical requirements" }).getByRole("button", { name: /R002/ }).click();
  await expect(requirementsPage.getByText(vagueRequirement, { exact: true }).first()).toBeVisible();
  await expect(requirementsPage.getByText("1/2", { exact: true }).first()).toBeVisible();
  const evidenceTrigger = page.getByRole("button", { name: /evidence .*швидко/i }).first();
  await focusByTab(page, evidenceTrigger);
  await page.keyboard.press("Enter");
  const drawer = page.getByRole("dialog", { name: /E\d+/ });
  await expect(drawer).toContainText("швидко");
  await expect(drawer).toContainText("Start offset");
  await expect(drawer).toContainText("End offset");
  await page.keyboard.press("Escape");
  await expect(drawer).toHaveCount(0);
  await expect(evidenceTrigger).toBeFocused();

  await navigate(page, "Specification");
  await expect(page.getByText("COMPUTED", { exact: true }).first()).toBeVisible();
  await navigate(page, "Product Quality");
  await expect(page.getByText("EXTERNAL_EVIDENCE_NOT_SUPPLIED", { exact: true })).toBeVisible();
  await capture(page, "a2-initial-unavailable-product-quality.png");
  await navigate(page, "Risk");
  await expect(page.getByText("CONFIRMED_PROBLEM_AND_RISK_INPUTS_NOT_AVAILABLE", { exact: true })).toBeVisible();
  await navigate(page, "Corrective Actions");
  await expect(page.getByText("CONFIRMED_PROBLEM_NOT_AVAILABLE", { exact: true })).toBeVisible();
  await navigate(page, "Process");
  await expect(page.getByText("FULL_MODEL_LIFECYCLE_NOT_INVOKED", { exact: true })).toBeVisible();
  await navigate(page, "Audit");
  await expect(page.getByRole("heading", { level: 2, name: "Full Model Audit" })).toBeVisible();
  await expect(page.locator('[data-audit-path="$.full_model"]')).toContainText("null");

  const newSpecification = page.getByRole("button", { name: "New specification" });
  await focusByTab(page, newSpecification);
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { level: 1, name: "Analyze specification" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Research result sections" })).toHaveCount(0);
  await expect(editor).toHaveValue("");

  // Scenario B — one controlled fixture request exposes all ten legal pages.
  const demoButton = page.getByRole("button", { name: "Load demonstration example" });
  await focusByTab(page, demoButton);
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main").getByRole("heading", { level: 1, name: "Overview" })).toBeVisible({ timeout: 180_000 });
  expect(requests).toHaveLength(2);
  expect(requests[1]).toEqual({
    case: "CONTROLLED_DEMO",
    scenario: { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" },
  });
  await expect(resultNavigation(page).getByRole("button")).toHaveText([...baseSections, "Reassessment", "Comparison"]);
  await expect(page.getByText("CONTROLLED_DEMO", { exact: true })).toBeVisible();
  await expect(page.getByText("CONTROLLED_RESEARCH_REFERENCE_SCENARIO / 1", { exact: true })).toBeVisible();
  await capture(page, "b1-controlled-demo-overview.png");

  await navigate(page, "Product Quality");
  await expect(page.getByText("OBSERVED_REFERENCE_INDICATOR", { exact: true })).toBeVisible();
  await expect(page.getByText("PREDICTED_PERFORMANCE_EFFICIENCY", { exact: true })).toBeVisible();
  await navigate(page, "Risk");
  await expect(page.getByText("RISK_IDENTIFIED", { exact: true }).first()).toBeVisible();
  await expect(page.getByText("1/16", { exact: true })).toBeVisible();
  await capture(page, "b2-controlled-demo-risk.png");
  await navigate(page, "Process");
  await expect(page.getByText("Current lifecycle successor", { exact: true })).toBeVisible();
  await expect(page.getByText("SATISFIED", { exact: true }).first()).toBeVisible();
  await expect(page.getByText(/does not authorize RELEASE or PROCEED/)).toBeVisible();
  await capture(page, "b3-controlled-demo-process.png");
  await navigate(page, "Audit");
  const auditBranch = page.locator('.audit-node--branch[data-audit-path="$.controlled_scenario"] > summary');
  await auditBranch.focus();
  await page.keyboard.press("Enter");
  await expect(auditBranch.locator("xpath=..")).toHaveAttribute("open", "");
  await capture(page, "b4-controlled-demo-audit-expanded.png", false);
  await navigate(page, "Reassessment");
  await expect(page.getByText("SPEC-TC06-REFERENCE / v1", { exact: true })).toBeVisible();
  await expect(page.getByText("SPEC-TC06-REFERENCE / v2", { exact: true })).toBeVisible();
  await navigate(page, "Comparison");
  await expect(page.getByRole("heading", { level: 2, name: "Model-produced comparisons" })).toBeVisible();
  for (const code of [
    "STRUCTURED_CHANGE_ONLY",
    "NO_DIRECTIONAL_QUALITY_INTERPRETATION",
    "NO_CAUSAL_EFFECT_INFERENCE",
    "NO_ACTION_SUCCESS_INFERENCE",
    "NO_STAKEHOLDER_INTENT_VALIDATION",
  ]) await expect(page.getByText(code, { exact: true }).first()).toBeVisible();

  const requestCountBeforeLocale = requests.length;
  await switchToUkrainian(page);
  await expect(page.getByRole("main").getByRole("heading", { level: 1, name: "Порівняння" })).toBeVisible();
  await expect(page.getByText("STRUCTURED_CHANGE_ONLY", { exact: true }).first()).toBeVisible();
  expect(requests).toHaveLength(requestCountBeforeLocale);
  await page.getByRole("navigation", { name: "Розділи результатів дослідження" }).getByRole("button", { name: "Огляд", exact: true }).click();
  await capture(page, "b5-controlled-demo-overview-uk.png");
  await switchToEnglish(page);

  // Scenario C — the canonical draft gates a second, formal REASSESSMENT request.
  await navigate(page, "Corrective Actions");
  const openReassessment = page.getByRole("button", { name: "Reassess revised specification" });
  await expect(openReassessment).toBeVisible();
  await openReassessment.click();
  const revisedEditor = page.getByRole("textbox", { name: "Revised specification" });
  const canonicalRevision = await revisedEditor.inputValue();
  await expect(revisedEditor).not.toHaveValue("");
  const reassess = page.getByRole("button", { name: "Analyze revised specification" });
  await revisedEditor.fill(`${canonicalRevision}\nДовільне неканонічне значення.`);
  await expect(reassess).toBeDisabled();
  await expect(page.getByText(/not the canonical external revision/)).toBeVisible();
  await revisedEditor.fill(canonicalRevision);
  await expect(reassess).toBeEnabled();
  await focusByTab(page, reassess);
  const reassessmentResponsePromise = page.waitForResponse((response) => (
    response.request().method() === "POST"
      && response.url().endsWith("/api/v1/analyze")
      && response.request().postDataJSON()?.case === "REASSESSMENT"
  ));
  await page.keyboard.press("Enter");
  const reassessmentResponse = await reassessmentResponsePromise;
  expect(reassessmentResponse.ok()).toBe(true);
  const reassessmentBody = await reassessmentResponse.json() as Record<string, unknown>;
  expect(reassessmentBody.analysis_case).toBe("REASSESSMENT");
  expect((reassessmentBody.full_model as Record<string, unknown>).comparisons).toHaveLength(4);
  await navigate(page, "Overview");
  await expect(page.getByText("REASSESSMENT", { exact: true }).first()).toBeVisible({ timeout: 180_000 });
  expect(requests).toHaveLength(3);
  expect(requests[2].case).toBe("REASSESSMENT");
  expect(requests[2].requirements).toEqual(canonicalRevision.split("\n").flatMap((text, index) => (
    text.trim().length > 0 ? [{ text: text.trim(), source_line: index + 1 }] : []
  )));
  expect(requests[2].prior_context).toEqual(expect.objectContaining({
    scenario: { id: "CONTROLLED_RESEARCH_REFERENCE_SCENARIO", version: "1" },
    initial_specification: expect.any(Object),
    predecessor_process_state: expect.any(Object),
    corrective_action_resolution: expect.any(Object),
    action_application: expect.any(Object),
    external_revision: expect.any(Object),
    revised_specification: expect.any(Object),
    evidence_reuse_decisions: expect.any(Array),
    comparisons: expect.any(Array),
  }));
  expect(requests[2]).not.toHaveProperty("summary");
  await expect(resultNavigation(page).getByRole("button")).toHaveText([...baseSections, "Reassessment", "Comparison"]);
  await navigate(page, "Reassessment");
  await expect(page.getByRole("heading", { level: 2, name: "Produced v2 results" })).toBeVisible();
  await expect(page.getByText("Changed by external revision", { exact: true })).toBeVisible();
  await capture(page, "c1-reassessment.png");
  await navigate(page, "Comparison");
  await expect(page.locator(".comparison-record")).toHaveCount(4);
  await expect(page.getByText("The comparison describes structured change only.")).toBeVisible();
  await capture(page, "c2-comparison.png");
  await switchToUkrainian(page);
  await capture(page, "c3-comparison-uk.png");
  expect(requests).toHaveLength(3);

  // Desktop-first minimum-width smoke: no page-level horizontal overflow.
  await page.setViewportSize({ width: 900, height: 1000 });
  await expect(page.getByRole("navigation")).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
  await expect(page.locator(".comparison-record").first()).toBeVisible();
});
