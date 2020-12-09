import ntpath
import time

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from io import BytesIO
from mimetypes import MimeTypes
from PIL import Image as PILImage

from wagtail.images.models import Image as WagtailImage

from networkapi.buyersguide.pagemodels.products.base import Product
from networkapi.buyersguide.pagemodels.products.general import GeneralProduct
from networkapi.buyersguide.pagemodels.products.software import SoftwareProduct
from networkapi.wagtailpages.pagemodels.base import Homepage
from networkapi.wagtailpages.pagemodels.products import (
    ProductPagePrivacyPolicyLink, ProductPage, SoftwareProductPage,
    GeneralProductPage, ProductPageCategory, BuyersGuidePage,
    RelatedProducts, ProductUpdates
)


class Command(BaseCommand):
    help = 'Migrate PNI Product models to Wagtail ProductPage types'

    # Get or create the buyersguidepage
    def get_or_create_buyers_guide(self):
        """
        Return the first BuyersGuidePage, or create a new one.
        """
        buyersguide_page = BuyersGuidePage.objects.first()
        if not buyersguide_page:
            # Create the buyersguide page.
            buyersguide_page = BuyersGuidePage()
            buyersguide_page.title = '*Privacy not included'
            buyersguide_page.slug = 'privacynotincluded'
            buyersguide_page.slug_en = 'privacynotincluded'
            homepage = Homepage.objects.first()
            homepage.add_child(instance=buyersguide_page)
            buyersguide_page.save_revision().publish()
        return buyersguide_page

    def debug_print(self, *messages):
        """For local debugging and testing only."""
        if settings.DEBUG:
            message = ' '.join([str(x) for x in messages])
            print(message)

    def handle(self, *args, **options):
        products = Product.objects.all()
        buyersguide_page = self.get_or_create_buyers_guide()

        for product in products:
            # 1. Create ProductPage out of this product
            product = product.specific  # Get the specific class

            # Always refresh the buyersguide_page to update treebeards pathing
            buyersguide_page.refresh_from_db()

            # Check if ProductPage exists. If it does, continue on.
            # This check will allow us to run this script more than once if needed
            if ProductPage.objects.filter(slug=product.slug).exists():
                self.debug_print(f"Product '{product.slug}' already exists, skipping.")
                continue

            if isinstance(product, SoftwareProduct):
                new_product_page = SoftwareProductPage()
                specific_fields = [
                    'medical_privacy_compliant', 'easy_to_learn_and_use', 'handles_recordings_how',
                    'recording_alert', 'recording_alert_helptext', 'medical_privacy_compliant_helptext',
                    'host_controls', 'easy_to_learn_and_use_helptext'
                ]
            elif isinstance(product, GeneralProduct):
                new_product_page = GeneralProductPage()
                specific_fields = [
                    'camera_device', 'camera_app', 'microphone_device', 'microphone_app',
                    'location_device', 'location_app', 'personal_data_collected',
                    'biometric_data_collected', 'social_data_collected',
                    'how_can_you_control_your_data', 'data_control_policy_is_bad',
                    'track_record_choices', 'company_track_record', 'track_record_is_bad',
                    'track_record_details', 'offline_capable', 'offline_use_description',
                    'uses_ai', 'ai_uses_personal_data', 'ai_is_transparent', 'ai_helptext'
                ]
            self.debug_print(f"Treating '{product.slug}' as {new_product_page.__class__.__name__}")

            # Apply the fields that are different or may cause issues if copied directly from one model to another
            new_product_page.slug_en = product.slug
            new_product_page.title = product.name
            new_product_page.title_en = product.name
            new_product_page.product_url = product.url
            new_product_page.cloudinary_image = product.cloudinary_image
            new_product_page.live = not product.draft  # If product is draft, it shall not be live.

            # These are the common fields between SoftwareProductPages and GeneralProductPages
            fields = specific_fields + [
                'slug', 'privacy_ding', 'adult_content', 'uses_wifi', 'uses_bluetooth',
                'review_date', 'company', 'blurb', 'price', 'worst_case',
                'signup_requires_email', 'signup_requires_phone',
                'signup_requires_third_party_account', 'signup_requirement_explanation',
                'how_does_it_use_data_collected', 'data_collection_policy_is_bad',
                'user_friendly_privacy_policy', 'show_ding_for_minimum_security_standards',
                'meets_minimum_security_standards', 'uses_encryption',
                'uses_encryption_helptext', 'security_updates', 'security_updates_helptext',
                'strong_password', 'strong_password_helptext', 'manage_vulnerabilities',
                'manage_vulnerabilities_helptext', 'privacy_policy', 'privacy_policy_helptext',
                'phone_number', 'live_chat', 'email', 'twitter'
            ]

            self.debug_print("\tSetting fields:")
            for field in fields:
                # Loop through every field for this product and copy the value
                # from the Product model to the Page model.
                self.debug_print("\t\t", field, " as ", getattr(product, field))
                setattr(new_product_page, field, getattr(product, field))

            # Get the image file field, and convert it into a WagtailImage object
            if product.image:
                # Check if there is an image file. If there isn't one, don't try to copy the
                # FieldFile to a WagtailImage object.
                try:
                    image_file = product.image.file
                except FileNotFoundError:
                    image_file = None

                if image_file:
                    mime = MimeTypes()
                    mime_type = mime.guess_type(product.image.file.name)  # -> ('image/jpeg', None)
                    if mime_type:
                        mime_type = mime_type[0].split('/')[1].upper()
                    else:
                        # Default to a JPEG mimetype.
                        mime_type = 'JPEG'
                    # Create an image out of the FileField.
                    pil_image = PILImage.open(product.image.file)
                    f = BytesIO()
                    pil_image.save(f, mime_type)
                    # Store the image as a WagtailImage object
                    new_image_name = ntpath.basename(product.image.file.name)
                    wagtail_image = WagtailImage.objects.create(
                        title=new_image_name,
                        file=ImageFile(f, name=new_image_name)
                    )
                    # Associate new_product_page.image with wagtail_image
                    new_product_page.image = wagtail_image

            # Add the new page as a child to BuyersGuidePage. This will add a
            # `path` to the new_product_page and place it in the Wagtail Tree
            # using Django Treebeard
            buyersguide_page.add_child(instance=new_product_page)

            # Save revision and/or publish so we can add Orderables to this page.
            new_product_page.save()
            new_product_page.save_revision()

            self.debug_print("\tCreated", new_product_page)

            # Loop through all the m2ms and create Orderable objects for this new page type
            # Add privacy policy links
            for privacy_link in product.privacy_policy_links.all():
                new_orderable = ProductPagePrivacyPolicyLink()
                new_orderable.page = new_product_page
                new_orderable.label = privacy_link.label
                new_orderable.url = privacy_link.url
                new_orderable.save()
                new_product_page.privacy_policy_links.add(new_orderable)
                self.debug_print("\tPrivacy Orderables added")
            # Add product categories
            for category in product.product_category.all():
                new_orderable = ProductPageCategory()
                new_orderable.product = new_product_page
                new_orderable.category = category
                new_orderable.save()
                new_product_page.product_categories.add(new_orderable)
                self.debug_print("\tCategory Orderables added")
            # Add updates
            for update in product.updates.all():
                new_orderable = ProductUpdates()
                new_orderable.page = new_product_page
                new_orderable.update = update
                new_orderable.save()
                new_product_page.updates.add(new_orderable)
                self.debug_print("\tUpdate Orderables added")

            # Attach a Votes object to each page if `Page.get_or_create_votes()` exists.
            if hasattr(new_product_page, 'get_or_create_votes'):
                new_product_page.get_or_create_votes()
                # Use .to_dict() to pull out the old aggregated votes
                product_dict = product.to_dict()
                votes = product_dict.get('votes', None)
                if votes:
                    self.debug_print(votes)
                    votes = votes.get('creepiness').get('vote_breakdown')
                    values = [x for x in votes.values()]
                    product_total = sum([x * ((i+1)*20-10) for i, x in enumerate(values)])
                    self.debug_print(f'\tOriginal votes: {values} (total score: {product_total})')
                else:
                    # Default vote "bin"
                    values = [0, 0, 0, 0, 0]
                    product_total = 0

            new_product_page.votes.set_votes(values)
            new_product_page.creepiness_value = product_total
            new_product_page.save()
            self.debug_print(f'\tNew product votes: {new_product_page.get_or_create_votes()}')

            if not product.draft:
                new_product_page.live = True
                new_product_page.save_revision().publish()
            else:
                new_product_page.save_revision()

            # Always good to fresh from db when using Django Treebeard.
            buyersguide_page.refresh_from_db()

        time.sleep(1)

        # Once all the ProductPages are added, add related_products
        # By writing a secondary for loop we can avoid attaching a legacy_product
        # to each ProductPage because they'll have slugs in common.
        self.debug_print("\nFinal step: Adding related products\n")

        # Loop through every ProductPage we now have.
        for product_page in ProductPage.objects.all():
            # Fetch the PNI Product that this page was created from.
            try:
                product = Product.objects.get(slug=product_page.slug)
            except Product.DoesNotExist:
                self.debug_print(f"Skipping {product_page} because a ProductPage.slug={product_page.slug} was not found")  # noqa
                continue
            # Loop through all the Product.related_products
            for related_product in product.related_products.all():
                try:
                    # Find the related ProductPage based on the correct slug.
                    related_page = ProductPage.objects.get(slug=related_product.slug)
                except ProductPage.DoesNotExist:
                    self.debug_print("Missing product page", product_page)
                    continue
                # Create a new Orderable for the Related Product. This provides
                # a higher quality editing experience for Wagtail editors/admins.
                new_related_product = RelatedProducts()
                new_related_product.page = product_page
                new_related_product.related_product = related_page
                new_related_product.save()
                product_page.related_product_pages.add(new_related_product)
                self.debug_print("\tAdded related product page:", related_page)
