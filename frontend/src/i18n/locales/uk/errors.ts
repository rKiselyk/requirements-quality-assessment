export const errors = {
  unknown: "Не вдалося виконати запит на аналіз.",
  codes: {
    EMPTY_SPECIFICATION: "Специфікація не містить непорожніх вимог.",
    MALFORMED_REQUIREMENT_INPUT: "Не вдалося прочитати введені вимоги.",
    INVALID_REASSESSMENT_CONTEXT: "Контекст повторного оцінювання відсутній або недійсний.",
    INVALID_CONTROLLED_DEMO_REQUEST: "Запит контрольованої демонстрації недійсний.",
    ANALYSIS_VALIDATION_FAILED: "Перевірка аналізу завершилася невдало.",
    ANALYSIS_INTERNAL_FAILURE: "Під час аналізу сталася неочікувана помилка.",
  },
} as const;
