from rest_framework.generics import ListAPIView, RetrieveAPIView

from networkapi.milestones.models import Milestone
from networkapi.milestones.serializers import MilestoneSerializer


class MilestoneListView(ListAPIView):
    """
    A view that permits a GET to allow listing of milestones
    in the database
    """
    def get_queryset(self):
        return Milestone.objects.all()

    serializer_class = MilestoneSerializer
    pagination_class = None


class MilestoneView(RetrieveAPIView):
    """
    A view that permits a GET request for a Milestone in the database
    """
    def get_queryset(self):
        return Milestone.objects.all()

    serializer_class = MilestoneSerializer
