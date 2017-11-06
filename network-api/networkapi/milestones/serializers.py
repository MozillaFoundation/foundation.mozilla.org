from rest_framework import serializers

from networkapi.milestones.models import Milestone


class MilestoneSerializer(serializers.ModelSerializer):
    """
    Serializes a Milestone object
    """
    class Meta:
        model = Milestone
        fields = (
            'id',
            'link_label',
            'link_url',
            'headline',
            'photo',
            'start_date',
            'end_date',
            'description'
        )
