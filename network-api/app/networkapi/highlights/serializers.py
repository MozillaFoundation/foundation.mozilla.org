from rest_framework import serializers

from networkapi.highlights.models import Highlight


class HighlightSerializer(serializers.ModelSerializer):
    """
    Serializes an Highlight Model
    """

    class Meta:
        model = Highlight
        fields = (
            'id',
            'title',
            'description',
            'link_url',
            'link_label',
            'image',
            'footer',
        )
