# Upgrading guidelines

This document describes aspects of the system which should be given particular attention when upgrading Wagtail or its dependencies.

## Upgrading Wagtail

### Snippet chooser customisation

Currently in Wagtail, when a snippet model implements the TranslatableMixin, the snippet chooser will allow editors to choose snippets in all the available languages. In most of the cases, we only want editors to choose the snippets in the default language as we handle the localisation in the template.

In order for snippet choosers to hide the translations and the locale filter, we implemented a custom DefaultLocaleSnippetChooseView based on `wagtail.admin.views.generic.chooser.BaseChooseView`. 

When upgrading Wagtail, please check if there are changes to [`wagtail.admin.views.generic.chooser.BaseChooseView`](https://github.com/wagtail/wagtail/blob/v4.1.6/wagtail/admin/views/generic/chooser.py#L103C1-L123C1) and update `DefaultLocaleSnippetChooseView` accordingly.
