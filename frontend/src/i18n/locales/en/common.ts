export const common = {
  app: {
    brand: "Requirements Quality Assessment",
    prototype: "Research Prototype",
  },
  language: {
    label: "Presentation language",
    switchTo: "Switch presentation language to {{language}}",
    uk: "Ukrainian",
    en: "English",
  },
  navigation: {
    label: "Research result sections",
    foundation: "Foundation",
    components: "Components",
    scientific: "Scientific primitives",
  },
  actions: {
    demo: "Demo action",
    primary: "Primary action",
    secondary: "Secondary action",
    quiet: "Quiet action",
    moreInformation: "More information",
    working: "Working…",
  },
  page: {
    title: "Research UI foundation",
    subtitle: "RUI-04 localization showcase — static presentation data only",
    notConnected: "Not connected to the analysis API",
    about: "About this demo",
    aboutTooltip: "This showcase does not submit an analysis.",
  },
  showcase: {
    title: "Foundation-only showcase",
    description: "Every value and state below is static demonstration content supplied to presentation components. No scientific result is calculated or inferred here.",
    shellEyebrow: "Shell and surfaces",
    foundation: "Foundation",
    sharedCard: "Shared card",
    sharedCardDescription: "A restrained surface for grouped research information.",
    reusableEyebrow: "Reusable controls",
    genericComponents: "Generic components",
    feedback: "Feedback and progress",
    disclosure: "Disclosure patterns",
    presentationOnly: "Presentation only",
    scientificPrimitives: "Scientific primitives",
  },
  table: {
    noRecords: "No records",
    scrollableRegion: "{{caption}}, scrollable table",
  },
  states: {
    loading: "Loading",
    unavailable: "Unavailable",
    noValue: "No value",
  },
  exactValue: {
    label: "Exact value",
  },
  evidence: {
    accessibleLabel: "{{kind}} evidence {{evidenceId}}{{sourceSuffix}}",
    sourceSuffix: ": {{sourceText}}",
  },
} as const;
