from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from networkapi.events.models import TitoEvent
from networkapi.mozfest.models import NewsletterSignupWithBackground, Ticket


class TitoEventSnippetViewSet(SnippetViewSet):
    model = TitoEvent
    icon = "tito"
    menu_order = 000
    menu_label = "Tito"
    menu_name = "Tito"
    list_display = (
        "title",
        "event_id",
    )
    search_fields = ("title", "event_id", "newsletter_question_id")


class TicketSnippetViewSet(SnippetViewSet):
    model = Ticket
    icon = "ticket"
    menu_order = 100
    menu_label = "Tickets"
    menu_name = "Tickets"
    list_display = (
        "name",
        "cost",
        "event",
        "sticker_text",
    )
    search_fields = ("name", "description", "cost", "button_text", "releases", "event", "sticker_text")


class NewsletterSignupWithBackgroundSnippetViewSet(SnippetViewSet):
    model = NewsletterSignupWithBackground
    icon = "newspaper"
    menu_order = 200
    menu_label = "Newsletter Signups"
    menu_name = "Newsletter Signups"
    list_display = (
        "name",
        "newsletter",
    )
    search_fields = ("name", "header", "description", "newsletter")


class MozfestViewSetGroup(SnippetViewSetGroup):
    items = (TitoEventSnippetViewSet, TicketSnippetViewSet, NewsletterSignupWithBackgroundSnippetViewSet)
    menu_icon = "mozfest"
    menu_label = "Mozfest"
    menu_name = "Mozfest"
    menu_order = 1300


register_snippet(MozfestViewSetGroup)
