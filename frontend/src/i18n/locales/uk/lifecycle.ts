export const lifecycle = {
  actions: {
    newSpecification: "Нова специфікація",
    tryAgain: "Спробувати ще раз",
  },
  analyzing: {
    title: "Аналіз специфікації виконується",
    description: "Модель оцінює подану специфікацію.",
    progressLabel: "Триває аналіз",
    resultNotice: "Результати з’являться після завершення аналізу.",
  },
  error: {
    title: "Не вдалося завершити аналіз",
  },
  result: {
    title: "Результат аналізу готовий",
    subtitle: "Канонічну відповідь збережено для сторінок результатів Research UI.",
    completed: "Аналіз завершено",
    boundary: "Докладне представлення результатів відкладено до RUI-07.",
    metadataTitle: "Метадані канонічної відповіді",
    analysisCase: "Випадок аналізу",
    contractVersion: "Версія контракту",
  },
} as const;
