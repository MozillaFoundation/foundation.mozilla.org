from django import template

from networkapi.wagtailpages.pagemodels.libraries.rcc.landing_page import RCCLandingPage
from networkapi.wagtailpages.pagemodels.libraries.research_hub.landing_page import (
    ResearchLandingPage,
)

register = template.Library()


@register.inclusion_tag("fragments/breadcrumbs.html", takes_context=True)
def research_breadcrumbs(context, include_self=False):
    page = context["page"]
    research_landing_page = ResearchLandingPage.objects.filter(locale=page.locale).first()
    page_ancestors = page.get_ancestors(include_self).descendant_of(research_landing_page, True)
    breadcrumb_list = [{"title": ancestor_page.title, "url": ancestor_page.url} for ancestor_page in page_ancestors]

    return {"breadcrumb_list": breadcrumb_list}


@register.inclusion_tag("fragments/breadcrumbs.html", takes_context=True)
def rcc_breadcrumbs(context, include_self=False):
    page = context["page"]
    rcc_landing_page = RCCLandingPage.objects.filter(locale=page.locale).first()
    page_ancestors = page.get_ancestors(include_self).descendant_of(rcc_landing_page, True)
    breadcrumb_list = [{"title": ancestor_page.title, "url": ancestor_page.url} for ancestor_page in page_ancestors]

    return {"breadcrumb_list": breadcrumb_list}
