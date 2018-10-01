from rest_framework import serializers
from django.forms.models import model_to_dict


class ProductSerializer(serializers.Serializer):
    def to_representation(self, instance):
        votes = []

        for range_product_vote in instance.range_product_votes.all():
            breakdown = {
                'attribute': 'creepiness',
                'average': range_product_vote.average,
                'vote_breakdown': {}
            }

            for vote_breakdown in range_product_vote.rangevotebreakdown_set.all():
                breakdown['vote_breakdown'][str(vote_breakdown.bucket)] = vote_breakdown.count

            votes.append(breakdown)

        for boolean_product_vote in instance.boolean_product_votes.all():
            breakdown = {
                'attribute': 'confidence',
                'vote_breakdown': {}
            }

            for vote_breakdown in boolean_product_vote.booleanvotebreakdown_set.all():
                breakdown['vote_breakdown'][str(vote_breakdown.bucket)] = vote_breakdown.count

            votes.append(breakdown)

        product_dict = model_to_dict(instance)
        product_dict['votes'] = votes

        return product_dict
