///////////////
jQuery( () => {
///////////////

const tabbedContent = $(`form .tab-content`);
const topLevel = (tabbedContent.length > 0) ? tabbedContent : $(`.content form`);

if (topLevel.length === 0) {
  // obviously, if we don't have an element to attach
  // the picker to, we might as well stop right now.
  return;
}

if (topLevel.attr(`class`) && topLevel.attr(`class`).indexOf(`search`) > -1) {
  // if the only forms on the page are search forms,
  // we're not actually dealing with page/snippets
  return;
}

/**
 * ...
 */
function filterForLocale(index, element) {
  var tc = element.textContent;
  var res = tc.match(/ \[\w\w\]/);
  if (res === null) return;

  var code = res[0],
      locale = code.replace(/[ \[\]]/g,'');

  // Verify this is a known locale and not a fluke,
  // using the global "langs" variable, which is an
  // array of all language codes specified in the
  // settings.LANGUAGES variable for Django.
  if (langs.indexOf(locale) === -1) return;

  // We do our show/hiding based on list items,
  // otherwise we're just "emptying" a list item
  // while leaving its spacing CSS intact.
  if (element.nodeName !== "LI") {
    element = $(element).closest("li")[0];
  }

  // Bootstrap an empty bin if we don't have one.
  if (!localisedElements[locale]) {
    localisedElements[locale] = [];
  }

  // Add this element to our bin, provided it had
  // not already been added.
  var bin = localisedElements[locale];
  if (bin.indexOf(element) === -1) {
    bin.push(element);
    element.classList.add(`l10n-hidden`);

    // also note that "field-col" elements may now look horribly
    // wrong, due to how Wagtail computes which of "col3"..."col12"
    // to use. Because wagtail-modeltranslation introduces many more
    // elements to show in an "inline" element, things that were
    // "col6" before end up being "col1", looking terribly wrong indeed.
    element.classList.remove(...columnCSS);
  }
}

/**
 * Build the set of fields-per-locale. Each set will receive
 * a button to toggle visibility for all fields in that set,
 * with the note that unlocalised content (such as images)
 * will always stay visible.
 */
function buildSets() {
  $(`li.object, div.field`, topLevel).each( filterForLocale );
}

/**
 * Build a locale picker bar, with buttons that toggle
 * visibility for each locale's fields.
 */
function buildLocaleToggler() {
  var bar = $(`<div class="locale-picker"><h2>View/edit fields for:</h2></div>`);
  var ul = $(`<ul class="locales"></ul>`);
  bar.append(ul);

  var toggles = {};
  locales.forEach( locale => {
    var li = $(`<li class="locale"><button class="locale-toggle">${locale}</button></li>`);
    ul.append(li);

    $(`button.locale-toggle`, li).each( (index, toggle) => {
      toggle.addEventListener(`click`, e => {
        e.preventDefault();
        toggle.classList.toggle(`showing-locale`);
        toggleLocale(locale);
      });

      toggles[locale] = toggle;
    });
  });

  bar.prependTo(topLevel);

  return toggles;
}

/**
 * This function allows either blind toggling
 * of a field's visibility, or explicitly
 * making visible/invisible based on the
 * value of `state` (a boolean).
 */
function toggleLocale(locale, state) {
  var action = `toggle`;

  if (state !== undefined) {
    action = state ? `remove` : `add`
  }

  localisedElements[locale].forEach(element => {
    element.classList[action](`l10n-hidden`);
  });
}

var default_locale = `en`;
var localisedElements = {};
var columnCSS = [`field-col`];
for (var i=1; i<=12; i++) { columnCSS.push(`col${i}`); }

// Build the sets that track which fields
// belong to which language code.
buildSets();

var locales = Object.keys(localisedElements).sort();

// If there are no locale sets, then there is
// no locale field picker to build, either.
if (locales.length === 0) return;

// If there are locale sets, make sure to
// enable at least the default locale after
// building and hiding all locale sets.
var localeToggler = buildLocaleToggler();
localeToggler[default_locale].click();

///////////////
});
///////////////
