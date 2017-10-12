from rest_framework import serializers

from networkapi.people.models import Person


class PersonSerializer(serializers.ModelSerializer):
    """
    Serializes a Person, including all many-to-many relations
    """
    affiliations = serializers.StringRelatedField(many=True)
    internet_health_issues = serializers.StringRelatedField(many=True)
    links = serializers.SerializerMethodField()

    def get_links(self, instance):
        return {
            'twitter': instance.twitter_url,
            'linkedIn': instance.linkedin_url,
            'interview': instance.interview_url,
        }

    class Meta:
        model = Person
        fields = (
            'name',
            'role',
            'location',
            'image',
            'links',
            'featured',
            'bio',
            'quote',
            'affiliations',
            'internet_health_issues',
            'partnership_logo',
        )
