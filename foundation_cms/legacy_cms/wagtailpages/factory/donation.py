from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from legacy_cms.wagtailpages.donation_modal import DonationModal, DonationModals


class DonationModalFactory(DjangoModelFactory):
    class Meta:
        model = DonationModal

    name = Faker("text", max_nb_chars=20)


class DonationModalsFactory(DjangoModelFactory):
    # note: plural!
    class Meta:
        model = DonationModals

    donation_modal = SubFactory(DonationModalFactory)
