from django.core.management.base import BaseCommand
from django.db.models import (
    Avg,
    IntegerField
)

from networkapi.buyersguide.models import (
    Product,
    RangeVote,
    BooleanVote,
    RangeProductVote,
    BooleanProductVote,
    RangeVoteBreakdown, BooleanVoteBreakdown)


class Command(BaseCommand):
    help = 'tally product votes and update Product records'

    # define the lower and upper values for filtering and
    # counting a product's totals in a given "bucket"
    range_filter_values = {
        '0': (1, 20),
        '1': (21, 40),
        '2': (41, 60),
        '3': (61, 80),
        '4': (81, 100)
    }

    def handle(self, *args, **options):
        products = Product.objects.all()

        for product in products:
            # generate a QuerySet for this product's creepiness votes
            creepiness_query_set = RangeVote.objects.filter(
                attribute='creepiness',
                product_id=product.id
            )

            # Calculate the total amount of votes for this product
            creepiness_vote_count = creepiness_query_set.count()

            # Calculate the average total creepiness score for this product, default to 50 if there aren't votes.
            creepiness_avg = creepiness_query_set.aggregate(
                Avg('value', output_field=IntegerField())
            )['value__avg'] if creepiness_vote_count > 0 else 50

            # define an object for recording this product's creepiness bucket totals
            creepiness_bucket_totals = {}

            # For each bucket group, filter votes on the low and high values, and record the count of each
            for creepiness_bucket in self.range_filter_values.keys():
                low, high = self.range_filter_values[creepiness_bucket]
                vote_count = creepiness_query_set.filter(
                    value__gte=low,
                    value__lte=high
                ).count()
                creepiness_bucket_totals[creepiness_bucket] = vote_count

            # get or create the ProductVote record for creepiness
            creepiness_product_vote, created = RangeProductVote.objects.get_or_create(
                product=product,
                attribute='creepiness',
                defaults={'votes': 0, 'average': 50}
            )

            # Set/update the total votes and average rating for the product.
            creepiness_product_vote.votes = creepiness_vote_count
            creepiness_product_vote.average = creepiness_avg
            creepiness_product_vote.save()

            # if this is a new product, create some VoteBreakdown records for it
            if created:
                for bucket in creepiness_bucket_totals.keys():
                    RangeVoteBreakdown.objects.create(
                        product_vote=creepiness_product_vote,
                        bucket=bucket,
                        count=0
                    )

            # update VoteBreakdown records with per bucket vote totals
            for vote_breakdown in creepiness_product_vote.rangevotebreakdown_set.all():
                vote_breakdown.count = creepiness_bucket_totals[str(vote_breakdown.bucket)]
                vote_breakdown.save()

            # Confidence
            # Define a QuerySet for confidence votes
            confidence_query_set = BooleanVote.objects.filter(
                attribute='confidence',
                product_id=product.id
            )

            # Calculate vote totals
            true_total = confidence_query_set.filter(value__exact=True).count()
            false_total = confidence_query_set.filter(value__exact=False).count()
            confidence_vote_count = true_total + false_total

            # get or create the ProductVote record for creepiness
            confidence_product_vote, created = BooleanProductVote.objects.get_or_create(
                product=product,
                attribute='confidence',
                defaults={'votes': 0}
            )

            confidence_product_vote.votes = confidence_vote_count
            confidence_product_vote.save()

            # if this is a new product, create some VoteBreakdown records for it
            if created:
                for bucket in (0, 1):
                    BooleanVoteBreakdown.objects.create(
                        product_vote=confidence_product_vote,
                        bucket=bucket,
                        count=0
                    )

            for vote_breakdown in confidence_product_vote.booleanvotebreakdown_set.all():
                vote_breakdown.count = true_total if vote_breakdown.bucket == 1 else false_total
                vote_breakdown.save()
