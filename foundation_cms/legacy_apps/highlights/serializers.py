from rest_framework import serializers

from foundation_cms.legacy_apps.highlights.models import Highlight


class WagtailImageSerializer(serializers.Serializer):
    def to_representation(self, image):
        return image.file.url


class HighlightSerializer(serializers.ModelSerializer):
    """
    Serializes an Highlight Model
    """

    image = WagtailImageSerializer()

    class Meta:
        model = Highlight
        fields = (
            "id",
            "title",
            "description",
            "link_url",
            "link_label",
            "image",
            "footer",
        )
