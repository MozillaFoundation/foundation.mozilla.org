from rest_framework import serializers
from networkapi.news.models import News


class NewsSerializer(serializers.ModelSerializer):

    """
    Serializes a News object
    """
    class Meta:
        model = News
        fields = (
            'headline',
            'outlet',
            'date',
            'link',
            'excerpt',
            'author',
            'thumbnail',
            'is_video',
            'featured',
        )
