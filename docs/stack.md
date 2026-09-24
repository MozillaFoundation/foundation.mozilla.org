# Stack

## HTML

HTML for the majority of the site is generated from Django/Wagtail templates and components.

## Frontend styleguide

This site has a [styleguide](https://foundation.mozilla.org/en/style-guide/), which can be refrenced for frontend development to note intended usage of exisitng styles and components.

## CSS

CSS is currently in a state of transition.
We are using custom [Sass](http://sass-lang.com/), mixed with the mofo-bootstrap theme found under `foundation_cms/legacy_apps/static/sass/mofo-bootstrap` while we also trying to move away from Bootstrap to [Tailwind CSS](https://tailwindcss.com/).
Reason for the transition to Tailwind is that it allows us to sync the design tokens defined by the design team with the available CSS utilities, which makes it easier for our implementation to stay true to the design system.
The following epic should give a better picture as to where we stand in this transition: https://app.zenhub.com/workspaces/mofo-engagement-585335eab729771d0736378d/issues/mozilla/foundation.mozilla.org/6989

We are utilizing the [Tailwind configuration file (`tailwind.config.js`)](https://tailwindcss.com/docs/configuration) to override some of the Tailwind's default design system options with our own.
For example, we define our own screen breakpoints, sizing scale and colors.
See the config file directly for more details.

All new CSS work should try to replace all use of Bootstrap and custom classes by applying the correct Tailwind utilities in the HMTL.

For more complex components, there is also `tailwind-plugins/components.js`.
We are also using `tailwind-plugins/components.js` to define Tailwind equivalents of Bootstrap classes (e.g. `.container` and `.row`).

## Design tokens (redesign frontend)

The redesign frontend's colors, type, spacing, and other design values come from `frontend/redesign/tokens/*.json`, vendored from the design team's token deliverable.
Run `yarn build:tokens` (from `frontend/redesign`) to generate two committed files from that JSON:

- `foundation_cms/static/scss/_tokens.scss`: CSS custom properties, for runtime use in component CSS.
- `foundation_cms/static/scss/settings/_tokens.scss`: a Sass `$tokens` map, for anything needing a real value at compile time, like a breakpoint.

Motion tokens (`tokens/motion.json`) are the one exception to the naming: they're generated with an `mzf-` prefix, e.g. `--mzf-motion-duration-base`, to match the names LP's own token build writes and its component CSS reads. Every other category is unprefixed, e.g. `--space-32`.

This does not run automatically. `docker compose up`, and `yarn dev`/`watch:css` within it, never call `build:tokens`, they just compile whatever `.scss` is already checked out. Since the two generated files are committed, a normal `git pull` keeps them current without needing to regenerate anything.

If you edit a token JSON file, run `yarn build:tokens` yourself and commit the regenerated output alongside your JSON change. CI's `check:tokens` check regenerates and diffs against what's committed, so a JSON change without a matching regeneration fails the build.

### Using tokens in a reskin

- In component CSS, read a token at runtime with `var(--token-name)`, e.g. `color: var(--color-accent-blue);`.
- Anywhere that needs a real value at compile time instead of a runtime CSS variable (a Foundation setting override, a media query), use `map.get($tokens, "token-name")`. This requires the file to have its own `@use "sass:map";` and `@import` of the generated `settings/_tokens.scss`, `@use` module access doesn't carry across files the way a plain `@import` does. See `_colors.scss` or `_type.scss` for the pattern.
- There is one breakpoint, `size-breakpoint-mobile` (768px). Don't route it through Foundation's `breakpoint()` mixin or add it to the `$breakpoints` map, that map's key order is load-bearing for existing `only`/`down` range queries elsewhere in the codebase, and inserting into it can silently change what they resolve to.
- New and reskinned components should follow LP's design system directly rather than Foundation's grid. After discussing with designers, the 12-column grid isn't part of the site refresh going forward, so there's no grid/token reconciliation to do, just build against the tokens and LP's own component reference.
- New and reskinned components are authored desktop-first, matching LP's own CSS: unconditional base rules are the desktop styling, and the mobile-specific override is wrapped in the `mobile-only` mixin from `_mixins.scss`. This is the opposite direction from the rest of the codebase, which is mobile-first via Foundation's `breakpoint()` mixin, that's expected since this is new/reskinned work following LP's system rather than an edit to an existing mobile-first component. The mobile-first, Foundation-based implementation is legacy at this point and will go away as components get reskinned.

## React

React is used _à la carte_ for isolated component instances (eg: a tab switcher) since the site is not designed as a single page application. This precludes the need for Flux architecture, or such libraries as React Router.

To add a React component, you can target a container element from `/foundation_cms/legacy_apps/static/js/main.js` and inject it.

## htmx

We have added the [`htmx.org`](https://htmx.org) javascript library to the project.
`htmx` allows us to combine server rendered HTML (as we have with Django templates) with dynamic updates on the frontend.

The main workflow of `htmx` is the following:

1. A trigger (e.g. button click) leads to an AJAX request to the backend (Django),
2. Django renders a template in response to the AJAX request and sends the HTML back,
3. `htmx` injects the HTML response into the DOM.

This workflow fits particularly nice into a Django project like this, because most of this can be configured with a few HTML attributes.

For more information see the [`htmx` docs](https://htmx.org/docs/).

## Django and Wagtail

Django powers the backend of the site, and we use Wagtail with Django to provide CMS features and functionality.

If you are defining a new page class for the site, make sure it inherits both the Wagtail `Page` class as well as the `FoundationMetadataPageMixin` mixin. The first is a general Wagtail requirement, and the latter ensures that page metadata used for SEO and the like is (generally) correct.

### Localization

We use [wagtail-localize](https://wagtail-localize.org/) for CMS content localization. Please see its documentation for more information.

#### Localiztion of numbers

We are using Django's [`L10N` setting](https://docs.djangoproject.com/en/4.0/ref/settings/#use-l10n) set to `True`.
This will also be the Django default starting in version 4.0 and can not be disabled starting version 5.0.

With `L10N = True`, Django will use a formatting depending on the active locale when rendering numbers and dates.
This can have impilcations when we dynamically render numbers into template that are meant for programmatic use, think `script` or `style` tags as well as attributes like `width` and `height` on the `img` tag.
Rendering localized value can lead to wrong behaviour.

Consider for example that in the German locale the decimal separator is a comma rather than a dot.
This can lead to misinterpretation of the number as a list or otherwise invalid value.

To ensure correct programmatic use of the rendered numbers, we need to prevent their localization.
The `unlocalize` template filter can be used to deactivate the localization of a number in the template.

See also: https://docs.djangoproject.com/en/4.1/topics/i18n/formatting/#controlling-localization-in-templates

### A/B testing

The project has [wagtail-ab-testing](https://github.com/torchbox/wagtail-ab-testing) setup. Out-of-the box we only get a "Visit page" goal event type which we can use to track when users visit a goal page. [Custom goal types](https://github.com/wagtail-nest/wagtail-ab-testing#implementing-custom-goal-event-types) need to be setup to track other events such as making a donation, submitting a form, or clicking a link.

## S3

All assets are stored on S3.

## File Structure

```
/
├── foundation_cms <- Django/Wagtail site code
│   ├── legacy_apps <- pre-redesign Django apps live within this directory
│   │   └── wagtailpages <- most of the pages using wagtail are here
│   ├── static <- compiled/source JS, SCSS, images, fonts for the redesign frontend
│   └── templates <- page templates and overrides
├── frontend <- yarn workspaces for frontend tooling
│   ├── legacy <- legacy frontend build tooling (Bootstrap/Sass era)
│   └── redesign <- redesign frontend (esbuild + Foundation Framework)
├── tests <- Playwright integration & visual regression tests
└── maintenance <- static maintenance-mode page
```

The templates are very scattered at the moment.
We are trying to localize all tempaltes to the location `foundation_cms/legacy_apps/templates`.
When ever you touch or create a template, please move it to / create it in this location and place it in the appropriate sub-directory, `pages` or `fragments`.
Create sub-directories under `pages` or `fragments` only when necessary and you have more than one template that needs to be grouped.

## Fundraise Up

This site uses [Fundraise Up](https://fundraiseup.com/) as a payment processor.

### Enabling Test Mode

Developers can enable Fundraise Up "test mode" by appending the query parameter `?fundraiseUpLiveMode=no` to the end of the current URL.

With live mode disabled, you can test functionality without the need of a real credit card.
Test card information will be given to you when completing the checkout process.
