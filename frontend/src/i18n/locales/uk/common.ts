export const common = {
  app: {
    brand: "Оцінювання якості вимог",
    prototype: "Дослідницький прототип",
  },
  language: {
    label: "Мова представлення",
    switchTo: "Перемкнути мову представлення на {{language}}",
    uk: "українську",
    en: "англійську",
  },
  navigation: {
    label: "Розділи результатів дослідження",
    foundation: "Основа",
    components: "Компоненти",
    scientific: "Наукові примітиви",
  },
  actions: {
    demo: "Демонстраційна дія",
    primary: "Основна дія",
    secondary: "Другорядна дія",
    quiet: "Непомітна дія",
    moreInformation: "Докладніше",
    working: "Виконується…",
  },
  page: {
    title: "Основа Research UI",
    subtitle: "Демонстрація локалізації RUI-04 — лише статичні дані представлення",
    notConnected: "Не підключено до API аналізу",
    about: "Про цю демонстрацію",
    aboutTooltip: "Ця демонстрація не надсилає запит на аналіз.",
  },
  showcase: {
    title: "Демонстрація лише основи",
    description: "Усі значення та стани нижче є статичним демонстраційним вмістом, переданим компонентам представлення. Тут не обчислюється і не виводиться жоден науковий результат.",
    shellEyebrow: "Оболонка та поверхні",
    foundation: "Основа",
    sharedCard: "Спільна картка",
    sharedCardDescription: "Стримана поверхня для згрупованої дослідницької інформації.",
    reusableEyebrow: "Повторно використовувані елементи керування",
    genericComponents: "Загальні компоненти",
    feedback: "Зворотний зв’язок і перебіг",
    disclosure: "Шаблони розкриття",
    presentationOnly: "Лише представлення",
    scientificPrimitives: "Наукові примітиви",
  },
  table: {
    noRecords: "Немає записів",
    scrollableRegion: "{{caption}}, прокручувана таблиця",
  },
  states: {
    loading: "Завантаження",
    unavailable: "Недоступно",
    noValue: "Значення відсутнє",
  },
  exactValue: {
    label: "Точне значення",
  },
  evidence: {
    accessibleLabel: "Доказ {{kind}} {{evidenceId}}{{sourceSuffix}}",
    sourceSuffix: ": {{sourceText}}",
  },
} as const;
