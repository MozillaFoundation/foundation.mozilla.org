from rest_framework.generics import ListAPIView, RetrieveAPIView

from networkapi.highlights.models import Highlight
from networkapi.highlights.serializers import HighlightSerializer


class HighlightListView(ListAPIView):
    """
    A view that permits a GET to allow listing of Highlight
    in the database
    """
    def get_queryset(self):
        return Highlight.objects.published()

    serializer_class = HighlightSerializer


class HighlightView(RetrieveAPIView):
    """
    A view that permits a GET request for an Highlight in the database
    """
    def get_queryset(self):
        return Highlight.objects.published()

    serializer_class = HighlightSerializer
