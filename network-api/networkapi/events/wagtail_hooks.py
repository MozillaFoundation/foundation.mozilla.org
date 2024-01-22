from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from networkapi.events.models import TitoEvent


class TitoEventSnippetViewSet(SnippetViewSet):
    model = TitoEvent
    icon = "tito"
    menu_order = 100
    menu_label = "Tito"
    menu_name = "Tito"
    list_display = (
        "title",
        "event_id",
    )
    search_fields = ("title", "event_id", "newsletter_question_id")


class EventsViewSetGroup(SnippetViewSetGroup):
    items = (TitoEventSnippetViewSet,)
    menu_icon = "calendar-check"
    menu_label = "Events"
    menu_name = "Events"


register_snippet(EventsViewSetGroup)
