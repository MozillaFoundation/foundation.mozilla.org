const LANGUAGES = {
  en: `English`,
  de: `Deutsch`,
  es: `Español`,
  fr: `Français`,
  pl: `Polski`,
  "pt-BR": `Português`,
};

let languageOptions = Object.keys(LANGUAGES).map((code) => {
  return {
    value: code,
    label: LANGUAGES[code],
  };
});

export const LANGUAGE_OPTIONS = languageOptions;
