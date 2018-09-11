from rest_framework import serializers


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

        return {
            'name': instance.name,
            'company': instance.company,
            'blurb': instance.blurb,
            'url': instance.url,
            'price': instance.price,
            'image': instance.image.url,
            'camera': instance.camera,
            'microphone': instance.microphone,
            'location': instance.location,
            'uses_encryption': instance.uses_encryption,
            'privacy_policy': instance.privacy_policy,
            'share_data': instance.share_data,
            'must_change_default_password': instance.must_change_default_password,
            'security_updates': instance.security_updates,
            'need_account': instance.need_account,
            'delete_data': instance.delete_data,
            'child_rules': instance.child_rules,
            'manage_security': instance.manage_security,
            'customer_support_easy': instance.customer_support_easy,
            'phone_number': instance.phone_number,
            'live_chat': instance.live_chat,
            'email': instance.email,
            'worst_case': instance.worst_case,
            'votes': votes
        }
