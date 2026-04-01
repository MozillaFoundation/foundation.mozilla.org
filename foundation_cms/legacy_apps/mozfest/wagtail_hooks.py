from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from foundation_cms.legacy_apps.wagtailcustomization.permissions import LegacySnippetViewSet
from foundation_cms.legacy_apps.events.models import TitoEvent
from foundation_cms.legacy_apps.mozfest.models import (
    NewsletterSignupWithBackground,
    Ticket,
)


class TitoEventSnippetViewSet(LegacySnippetViewSet):
    model = TitoEvent
    icon = "tito"
    menu_order = 000
    menu_label = "Tito (Legacy)"
    menu_name = "Tito (Legacy)"
    list_display = (
        "title",
        "event_id",
        "newsletter_question_id",
    )
    search_fields = ("title", "event_id", "newsletter_question_id")
    ordering = ("title",)


class TicketSnippetViewSet(LegacySnippetViewSet):
    model = Ticket
    icon = "ticket"
    menu_order = 100
    menu_label = "Tickets (Legacy)"
    menu_name = "Tickets (Legacy)"
    list_display = (
        "name",
        "cost",
        "event",
        "group",
        "sticker_text",
    )
    search_fields = ("name", "description", "group")
    ordering = ("name", "event", "group", "cost")


class NewsletterSignupWithBackgroundSnippetViewSet(LegacySnippetViewSet):
    model = NewsletterSignupWithBackground
    icon = "newspaper"
    menu_order = 200
    menu_label = "Newsletter Signups (Legacy)"
    menu_name = "Newsletter Signups (Legacy)"
    list_display = (
        "name",
        "newsletter",
    )
    search_fields = ("name", "newsletter")
    ordering = ("name",)


class MozfestViewSetGroup(SnippetViewSetGroup):
    items = (TitoEventSnippetViewSet, TicketSnippetViewSet, NewsletterSignupWithBackgroundSnippetViewSet)
    menu_icon = "mozfest"
    menu_label = "Mozfest (Legacy)"
    menu_name = "Mozfest (Legacy)"
    menu_order = 1300


register_snippet(MozfestViewSetGroup)
