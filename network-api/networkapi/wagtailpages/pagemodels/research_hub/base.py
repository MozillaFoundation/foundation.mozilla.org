from django.apps import apps

from networkapi.wagtailpages.pagemodels.base import BasePage


class ResearchHubBasePage(BasePage):
    ...

    class Meta:
        abstract = True
