from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist


def get_product_vote_information(product):
    votes = {}
    confidence_vote_breakdown = {}
    creepiness = {'vote_breakdown': {}}

    try:
        # Get vote QuerySets
        creepiness_votes = product.range_product_votes.get(attribute='creepiness')
        confidence_votes = product.boolean_product_votes.get(attribute='confidence')

        # Aggregate the Creepiness votes
        creepiness['average'] = creepiness_votes.average
        for vote_breakdown in creepiness_votes.rangevotebreakdown_set.all():
            creepiness['vote_breakdown'][str(vote_breakdown.bucket)] = vote_breakdown.count

        # Aggregate the confidence votes
        for boolean_vote_breakdown in confidence_votes.booleanvotebreakdown_set.all():
            confidence_vote_breakdown[str(boolean_vote_breakdown.bucket)] = boolean_vote_breakdown.count

        # Build + return the votes dict
        votes['creepiness'] = creepiness
        votes['confidence'] = confidence_vote_breakdown
        BooleanVote = apps.get_model('buyersguide', 'BooleanVote')
        votes['total'] = BooleanVote.objects.filter(product=product).count()
        return votes

    except ObjectDoesNotExist:
        # There's no aggregate data available yet, return None
        return None

    except AttributeError:
        # FIXME: This is a new general/software product that doesn't have voting hooked up yet
        return None
