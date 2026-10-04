export const input = {
  pageTitle: "Analyze specification",
  pageSubtitle: "Provide one requirement per physical line. Your specification remains editable before analysis.",
  ordinary: {
    title: "Specification input",
    description: "Paste requirements or choose a UTF-8 plain-text file. Both paths follow the same parsing rules.",
    or: "or",
  },
  file: {
    label: "Drop specification here or choose a file",
    description: "UTF-8 .txt or plain-text files only. The file is read in this browser and is not uploaded when selected.",
    reading: "Reading selected file: {{fileName}}",
    selected: "Selected file: {{fileName}}",
  },
  editor: {
    label: "Paste or edit requirements",
    hint: "Each non-empty physical line is one requirement. Leading and trailing whitespace is removed; blank lines are ignored.",
    placeholder: "Enter the first requirement\nEnter the second requirement",
  },
  preview: {
    title: "Requirement preview",
    count_one: "Parsed requirements: {{count}}",
    count_other: "Parsed requirements: {{count}}",
    sourceLine: "Source line {{line}}",
    empty: "No non-empty requirements to preview.",
  },
  actions: {
    analyze: "Analyze",
    clear: "Clear specification",
    loadDemo: "Load demonstration example",
  },
  validation: {
    empty: "Enter at least one non-empty requirement.",
    unsupported: "Choose a supported UTF-8 .txt or plain-text file.",
    unreadable: "The file could not be read as UTF-8 plain text. Choose another file.",
  },
  demo: {
    title: "Controlled research demonstration",
    description: "This separate, opt-in demonstration uses predefined research fixture data, including additional Full Model inputs that belong to the fixture.",
    boundary: "Those values are not inferred from your text, cannot be edited here, and are not part of the default specification workflow.",
  },
} as const;
