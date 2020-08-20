## Stack

### HTML

HTML for the majority of the site is generated from Django/Wagtail templates and components.

### CSS

CSS is generated from [Sass](http://sass-lang.com/). The [Mofo Bootstrap](https://github.com/mozilla/mofo-bootstrap) theme is pulled in by default.

### React

React is used _à la carte_ for isolated component instances (eg: a tab switcher) since this is not a single page application, but rather a static generated website. This precludes the need for Flux architecture, or such libraries as React Router.

To add a React component, you can target a container element from `/source/js/main.js` and inject it.

### Django and Wagtail

Django powers the backend of the site, and we use Wagtail with Django to provide CMS features and functionality.

If you are defining a new page class for the site, make sure it inherits both the Wagtail `Page` class as well as the `FoundationMetadataPageMixin` mixin. The first is a general Wagtail requirement, and the latter ensures that page metadata used for SEO and the like is (generally) correct.

#### localization

We use [wagtail-modeltranslations](https://github.com/infoportugal/wagtail-modeltranslation) for CMS content localization. Please see its documentation for more information.

#### A/B testing

We use [wagtail-experiments](https://github.com/torchbox/wagtail-experiments) for CMS-based A/B testing. Please see its documentation for more information.

### S3 and Cloudinary

Most assets are stored on S3. Buyers Guide images are hosted on Cloudinary.


### File Structure

```
/
├── dest <- Compiled code generated from source. Don't edit!
├── network-api <- Django site code
│   ├── networkapi <- Django apps live within this directory
        └── wagtailpages <- most of the pages using wagtail are here
│   └── templates <- page templates and overrides
├── locales <- Localized strings (Java .properties syntax)
├── scripts <- Scripts run by npm tasks
└── source <- Source code
    ├── images <- Image assets
    ├── js <- JS code
    │   └── components <- React components
    ├── json <- JSON for static data sets
    │   └── temp <- JSON pulled from web services. Don't commit!
    └── sass <- Sass code
```
