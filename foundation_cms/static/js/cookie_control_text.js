// Localized text for Cookie Control v9 (Civic UK)
// English is the default; other locales only need keys that differ.
// CookieControl text keys: https://cookiecontrol.com/docs/v9/

const LOCALE_TEXT = {
  en: {
    text: {
      title: "Privacy Preference Center",
      intro:
        "When you visit any website, it may store or retrieve information on your browser, mostly in the form of cookies. This information might be about you, your preferences or your device and is mostly used to make the site work as you expect it to. The information does not usually directly identify you, but it can give you a more personalized web experience. Because we respect your right to privacy, you can choose not to allow some types of cookies. Click on the different category headings to find out more and change our default settings. However, blocking some types of cookies may impact your experience of the site and the services we are able to offer.",
      notifyTitle: "Help Mozilla with Analytics",
      notifyDescription:
        "We use some essential cookies to make this website. We’d like to set additional cookies to understand how you use mozillafoundation.org. Your settings improve our services.",
      accept: "Accept Analytics Cookies",
      reject: "Reject Analytics Cookies",
      acceptSettings: "Allow All",
      rejectSettings: "Reject All",
      necessaryTitle: "Necessary Cookies",
      necessaryDescription:
        "These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information.",
      settings: "Consent Settings",
      closeLabel: "Close",
    },
    optionalCookies: [
      {
        name: "wip",
        label: "[WIP] Label for Optional Cookies",
        description: "[WIP] Description for optional cookies.",
      },
    ],
  },
  // Civic doesn't accept hyphenated codes
  // fy-NL and pt-BR are shortened to "fy" and "pt"
  ca: { text: { title: "[WIP] Títol (CA)" } },
  de: { text: { title: "[WIP] Titel (DE)" } },
  es: { text: { title: "[WIP] Título (ES)" } },
  fr: { text: { title: "[WIP] Titre (FR)" } },
  fy: { text: { title: "[WIP] Titel (FY)" } },
  nl: { text: { title: "[WIP] Titel (NL)" } },
  pl: { text: { title: "[WIP] Tytuł (PL)" } },
  pt: { text: { title: "[WIP] Título (PT)" } },
  sw: { text: { title: "[WIP] Kichwa (SW)" } },
};

export default LOCALE_TEXT;
