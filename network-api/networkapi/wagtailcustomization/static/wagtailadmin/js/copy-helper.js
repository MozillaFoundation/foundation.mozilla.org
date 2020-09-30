// Which locales are we dealing with?
const main = wagtailModelTranslations.defaultLanguage;
const languages = wagtailModelTranslations.languages.map((v) =>
  v.replace(`-`, `_`)
);

// Which fields are going to be potential deal-breakers?
const fields = Object.fromEntries(
  Array.from(
    document.querySelectorAll(`.content input[type=text]`)
  ).map((e) => [e.getAttribute(`name`), e])
);

// 1: Give staff a button that lets them reveal all locale fields, so they can
// manually edit any field to be any value they want.
const toggle = document.querySelector(`.locale.helper.button`);

toggle.addEventListener(`click`, () => {
  document.querySelectorAll(`.locale-picker .locale-toggle`).forEach((btn) => {
    if (!btn.classList.contains(`showing-locale`)) btn.click();
  });
});

// 2: Also give staff a button that lets them just copy whatever is in the
// [en] field(s) to all the other locales.
const sync = document.querySelector(`.synchronize.helper.button`);

sync.addEventListener(`click`, () => {
  Object.values(fields).forEach((field) => {
    const name = field.getAttribute(`name`);
    const code = languages.find((v) => name.includes(`_${v}`));
    if (code === main) return;
    field.value = fields[name.replace(`_${code}`, `_${main}`)].value;
  });
});

// Are there any errors? If so, we need to immediately reveal all fields
if (document.querySelectorAll(`p.error-message`).length !== 0) {
  toggle.click();
}
