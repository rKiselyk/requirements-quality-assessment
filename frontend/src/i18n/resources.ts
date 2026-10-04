import { common as enCommon } from "./locales/en/common";
import { input as enInput } from "./locales/en/input";
import { assessment as enAssessment } from "./locales/en/assessment";
import { productQuality as enProductQuality } from "./locales/en/productQuality";
import { risk as enRisk } from "./locales/en/risk";
import { process as enProcess } from "./locales/en/process";
import { audit as enAudit } from "./locales/en/audit";
import { errors as enErrors } from "./locales/en/errors";
import { limitations as enLimitations } from "./locales/en/limitations";
import { lifecycle as enLifecycle } from "./locales/en/lifecycle";
import { common as ukCommon } from "./locales/uk/common";
import { input as ukInput } from "./locales/uk/input";
import { assessment as ukAssessment } from "./locales/uk/assessment";
import { productQuality as ukProductQuality } from "./locales/uk/productQuality";
import { risk as ukRisk } from "./locales/uk/risk";
import { process as ukProcess } from "./locales/uk/process";
import { audit as ukAudit } from "./locales/uk/audit";
import { errors as ukErrors } from "./locales/uk/errors";
import { limitations as ukLimitations } from "./locales/uk/limitations";
import { lifecycle as ukLifecycle } from "./locales/uk/lifecycle";

export const resources = {
  uk: { common: ukCommon, input: ukInput, assessment: ukAssessment, productQuality: ukProductQuality, risk: ukRisk, process: ukProcess, audit: ukAudit, errors: ukErrors, limitations: ukLimitations, lifecycle: ukLifecycle },
  en: { common: enCommon, input: enInput, assessment: enAssessment, productQuality: enProductQuality, risk: enRisk, process: enProcess, audit: enAudit, errors: enErrors, limitations: enLimitations, lifecycle: enLifecycle },
} as const;

export const namespaces = ["common", "input", "assessment", "productQuality", "risk", "process", "audit", "errors", "limitations", "lifecycle"] as const;
