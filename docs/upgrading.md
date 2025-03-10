# Upgrading guidelines

This document describes aspects of the system which should be given particular attention when upgrading Wagtail or its dependencies.

## Upgrading Wagtail

### Snippet chooser customisation

Currently in Wagtail, when a snippet model implements the TranslatableMixin, the snippet chooser will allow editors to choose snippets in all the available languages. In most of the cases, we only want editors to choose the snippets in the default language as we handle the localisation in the template.

In order for snippet choosers to hide the translations and the locale filter, we implemented a custom DefaultLocaleSnippetChooseView based on `wagtail.admin.views.generic.chooser.BaseChooseView`. 

When upgrading Wagtail, please check if there are changes to [`wagtail.admin.views.generic.chooser.BaseChooseView`](https://github.com/wagtail/wagtail/blob/v4.2.4/wagtail/admin/views/generic/chooser.py#L150-L169) and update `DefaultLocaleSnippetChooseView` accordingly.

### Page types report

A pages types usage report has been added on `legacy_apps.reports.views`, which will be incorporated as [part of core on v6.0](https://github.com/wagtail/wagtail/pull/10850). Once that is added, the custom report should be removed.

### Localisation utility

The `localize_queryset` utility function on `legacy_apps.wagtailpages.utils` has been incorporated [into core](https://github.com/wagtail/wagtail/pull/11274). Once that has been released, the implementation here should be removed in favour of the core one.


## wagtail-ab-testing

In order to make `wagtail-ab-testing` compatible with our CSP, the main script and template tag had to be overwritten. The script on `templates/wagtail_ab_testing/script.html` was modified to pass values through a `json_script` tag (as [Django recommends](https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#json-script)) and a `nonce` was added to the scripts.

The `wagtail_ab_testing_script` template tag was rewritten at `legacy_apps.wagtailcustomization.templatetags.wagtailcustom_tags` to pass the request to the script so that it can pick up the `nonce` value from `request` (`request.csp_nonce`).
