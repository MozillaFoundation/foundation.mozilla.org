from django.conf import settings

from legacy_cms.wagtailpages.models import Petition

from .abstract import CTAFactory


class PetitionFactory(CTAFactory):
    class Meta:
        model = Petition

    campaign_id = settings.PETITION_TEST_CAMPAIGN_ID
