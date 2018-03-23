# Minisites in Wagtail

This document explains how the wagtail `minisites` app works with respect to the "networkapi" Django/Mezzanine instance.

The base app has the following directory structure:
```
- minisites
  |- migrations
  |  `- standard django migration files
  |
  |- templates
  |  `- minisites
  |     |- blocks
  |     |  `- block template .html files
  |     |- tags
  |     |  |- cta
  |     |  |  `- dir with some cta-tag related html fragments
  |     |  `- template-tag-related html fragments
  |     `- page template .html files
  |
  |- templatetags
  |  `- mini_site_tags.py
  |
  |- customblocks.py
  |- models.py
  `- README.md
```

# The basic minisite app architecture

## Page types

The minisites app defines four page models in the following hierarchy:

```
- ModularPage
  `- MiniSiteNameSpace
     |- OpportunityPage
     `- CampaignPage
```

#### 1. ModularPage

Houses all basic functionality, and is not intended for actual page creation. This class determines all the various StreamField blocks that can be used in subclassing pages.

Its template in `minisites/templates/minisites/modular_page.html` defines the full HTML page for any minisite page, with placeholder blocks for actual content.

#### 1.1 MiniSiteNameSpace

Adds minisite specific context variables for templating purposes, and is used as namespace 'root'. This page type can only have `OpportunityPage` and `CampaignPage` as children.

Its template in `minisites/templates/minisites/mini_site_page.html` has concrete definitions for all the mini-site-relevant blocks that pages may need.

#### 1.1.1 OpportunityPage

Represents a page in an "opportunity" minisite. This page can only have other `OpportunityPage` instances as children. This page has a `cta` property that can point to a `SignUp` snippet.

Its template in `minisites/templates/minisites/opportunity_page.html` is an empty extension on the minisite template.

#### 1.1.2 CampaignPage

Represents a page in a "campaign" minisite. This page can only have other `CampaignPage` instances as children. This page has a `cta` property that can point to a `Petition` snippet.

Its template in `minisites/templates/minisites/campaign_page.html` is an empty extension on the minisite template.

### CTA types

There are two CTA types defined for use in the campaign and opportunity pages. These CTA are defined as Wagtail "snippets", which makes them independent data models that can be administered independent of pages, with any number of pages able to point to some specific CTA instance.

The base CTA model has a title, header, description, and a newsletter identifier field.

#### 1. Signup

This is an empty subclass of CTA, as the base fields already cover the signup CTA case.

#### 2. Petition

This is a subclass of CTA that adds checkbox labels and google form identifiers for ensuring that petition form data can be captured in a specific google form. See its definition in `models.py` for the full list of fields this CTA makes use of.


## Stream blocks

In addition to the standard Wagtail-supplied blocks, the `customblocks.py` files defines the following custom blocks that can be used to build out content on pages:

#### 1. LinkButtonBlock

This block sets up a button that links out to a URL, using `networkapi/templates/minisites/blocks/link_button_block.html` as its rendering template.

#### 2. ImageTextBlock

This block sets up a text-with-image (image can be placed either right or left of the text), using `networkapi/templates/minisites/blocks/image_text_block.html` as its rendering template.

#### 3. VerticalSpacerBlock

This is a purely cosmetic block, effecting vertical whitespace as specified in `rem` units. It uses `networkapi/templates/minisites/blocks/vertical_spacer_block.html` as its rendering template.

#### 4. iFrameBlock

This is identical to the `VideoBlock`, but effects a straight-up iframe element, using `networkapi/templates/minisites/blocks/iframe_block.html` as its rendering template.

#### 5 .VideoBlock

This is an embed block that yields an iframe to an online video, with explicit width/heigh dimensions in pixels. It uses `networkapi/templates/minisites/blocks/video_block.html` as its rendering template.

## Template tags

In addition to standard wagtail tags, the minisites app defines two fairly important tags, which are used in the minisite templates:

#### `{% mini_site_sidebar page %}`

Used in the modular page template, this tag is responsible for building a menu, or not, depending on the actual page getting rendered.

The logic for this tag is found in `minisites/templatetags/mini_site_tags.py`, in the `def mini_site_sidebar(context, page):` definition.

Its code block computes various aspects of a minisite (root, children, singleton status, etc.) and is then rendered using the template found in `networkapi/templates/minisites/tags/mini_site_sidebar.html`.

This template has a shortcut that simply outputs "nothing" if the minisite page in question is a `singleton_page: True`.

#### `{% cta page %}`

Used in the minisite template, this tag will effect a signup or petition div element with all the appropriate `data-...` attributes for our React application to read in and convert into an active CTA form.

The logic for this tag is found in `minisites/templatetags/mini_site_tags.py`, in the `def cta(context, page):` definition.

Its code block simply sets up a context with the cta, and its Python class name, and is then rendered using the template found in `networkapi/templates/minisites/tags/cta.html`, which is a switching template, falling through to either `networkapi/templates/minisites/tags/cta/signup.html` or `networkapi/templates/minisites/tags/cta/peition.html`, depending on the CTA class name.

# Concrete use

As Wagtail does not come with any specific default layout, I created a homepage called `Wagtail site root` and then created two namespace pages under that:

```
Wagtail site root
 |- MiniSiteNameSpace(name='campaigns', draft=True)
 `- MiniSiteNameSpace(name='opportunity', draft=True)
```

These namespace pages are effectively placeholders for future work (where we can auto-generate the list of all campaign and opportunity minisites for accessibility/ease of navigation at some later point), with wagtail automatically creating namespaced URLs for any subpages: any child of the `campaigns` page will automatically be `.../campaigns/page-title`, and any child of the `opportunities` page will automatically be `.../opportunity/page-title`.

Both `campaigns` and `opportunity` were then given child pages of `CampaignPage` and `OpportunityPage` types, respectively, mirroring the current minisite conte found on the foundation.mozilla.org when looking at the page admin.
