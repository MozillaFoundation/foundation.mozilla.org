from rest_framework import serializers

from networkapi.homepage.models import (
    Homepage,
    HomepageLeaders,
    HomepageNews,
    HomepageHighlights,
)
from networkapi.people.serializers import PersonSerializer
from networkapi.news.serializers import NewsSerializer
from networkapi.highlights.serializers import HighlightSerializer


def serialize_relation(
    homepage_obj,
    through_model,
    related_field_name,
    related_serializer,
):
    """
    Returns a list of serialized related objects that are related to the
    homepage

    :param homepage_obj: is the instance that we want to seialize related
    objects for
    :param through_model: is the model class that represents the relation (not
    the model of the related object itself)
    :param related_field_name: is the field name on the `through_model` that
    is a foreign key pointing to the model related to the homepage
    :param related_serializer: is the serializer class to use to serialize the
    related model instance
    :returns: list of serialized related model instances
    """

    related_objs = []
    relation = (
        through_model.objects
        .select_related(related_field_name)
        .order_by('_order')
        .filter(homepage=homepage_obj)
    )

    for related_field in relation:
        related_objs.append(getattr(related_field, related_field_name))

    return related_serializer(related_objs, many=True).data


class HomepageSerializer(serializers.ModelSerializer):
    """
    Serializes a single (the only) homepage object including its
    related models using their default serializers
    """
    leaders = serializers.SerializerMethodField()

    def get_leaders(self, instance):
        return serialize_relation(
            instance,
            HomepageLeaders,
            'leader',
            PersonSerializer
        )

    highlights = serializers.SerializerMethodField()

    def get_highlights(self, instance):
        return serialize_relation(
            instance,
            HomepageHighlights,
            'highlights',
            HighlightSerializer
        )

    news = serializers.SerializerMethodField()

    def get_news(self, instance):
        return serialize_relation(
            instance,
            HomepageNews,
            'news',
            NewsSerializer
        )

    class Meta:
        model = Homepage
        fields = ('leaders', 'news', 'highlights',)
