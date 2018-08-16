# (Temporary) localised content in Wagtail

This document exists primarily because the current localisation approach is at best a patch to ensure there is _some_ localisation possible of Wagtail content in lieu of an official localisation solution that would ideally take the form of:

- An API for retrieving strings tied to specific pages using a unique page id,
- a mechanism to send those strings to Pontoon, or similar translation/localisation community
- a mechanism to receive translations from Pontoon (or similar service)
- an API for instructing wagtail which localised strings correspond to which original strings, applicable to which locale.

While Wagtail forms a plan of attack around tackling this, we need a localisation solution, and so we have implemented the following:

- `wagtail-modeltranslation` is used to enable content localisation based on a `LANGUAGE_CODE` default language identifier, and `LANGUAGES` list of tuples (of the form `('code', 'full name of locale')`).
- a custom javascript library that improves usability by allowing users of the CMS to hide/reveal localisable fields based on the language they belong to.

The modeltranslation library adds localised URLs to Wagtail, interjecting the locale code in the URL betewen the host domain and the content path, such that a url like:

    https://foundation.mozilla.org/campaigns/aadhaar

with "en" as locale, becomes:

    https://foundation.mozilla.org/en/campaigns/aadhaar

Additionally, there is now a `translations.py` file in the `wagtailpages` app that describes which models should have which fields automatically added to the set of localizable fields. This is, quite wisely, tracked in separate tables, so that removing wagtail-modeltranslations does not lead to a complete loss of all pages ever made, or massive migrations beyond "drop the translation wrapper tables". 

The [wagtail-modeltranslation](https://github.com/infoportugal/wagtail-modeltranslation) README.md covers all the steps taken to enable this on our end in, so please give that a read-over as well.

There is an open PR over on https://github.com/infoportugal/wagtail-modeltranslation/pull/211 which was opened to put our usability script in the modeltranslation package itself, however that PR has not landed at the time of writing this document, and so in order to land the PR that this document is in, the updated `wagtailhooks.py` that was necessary to get access to some of the settings over in the client environment has been manually added to a special app called `wagtail-l10n-customization`.

This special app has the following dir structure and content:

    wagtail-l10n-customization
      |- static
      |   |-css
      |   |  `-language_toggles.css : styling for the UX improvements
      |   `-js
      |      `-language_toggles.js : UX improvements for working with localisable fields
      `- wagtail_hooks.py : hooks into wagtail that load the UX improver in /cms

In order to ensure that things deploy smoothly, both the `Procfile` and the `tasks.py` have been updated with instructions specific to wagtail-modeltranslation use, so in the interest of knowing where to look when it comes time to take this back out, all the relevant changes happened by landing the following PR:

https://github.com/mozilla/foundation.mozilla.org/pull/1566