# This file is made to loop through all existing PNI products and update the following fields to richtext: 
# - Track record description
# - How does the company use this data?
# - How can you control your data?
# - General AI description
# - Manages security vulnerabilities Description

from django.db import migrations
from networkapi.wagtailpages.utils import get_default_locale


# Forward migration content handler
def update_fields_to_rich_text(product_qs):

    for product in product_qs:
        
        # If the page has no fields that need updating, do not save. This will speed up the process.
        needs_saving = False

        if hasattr(product, 'how_does_it_use_data_collected') and product.how_does_it_use_data_collected != "":
            product.how_does_it_use_data_collected = f"<p> {product.how_does_it_use_data_collected} </p>"
            needs_saving = True

        elif hasattr(product, 'manage_vulnerabilities_helptext') and product.manage_vulnerabilities_helptext != "":
            product.manage_vulnerabilities_helptext = f"<p> {product.manage_vulnerabilities_helptext} </p>"
            needs_saving = True

        elif hasattr(product, 'track_record_details') and product.track_record_details != "":
            product.track_record_details = f"<p> {product.track_record_details} </p>"
            needs_saving = True

        elif hasattr(product, 'offline_use_description') and product.offline_use_description != "":
            product.offline_use_description = f"<p> {product.offline_use_description} </p>"
            needs_saving = True

        elif hasattr(product, 'ai_helptext') and product.ai_helptext != "":
            product.ai_helptext = f"<p> {product.ai_helptext} </p>"
            needs_saving = True

        if needs_saving:
            product.save()
            print(f"Saved product: {product.title}")




def gather_products_and_update_fields(apps, schema):
    GeneralProductPage = apps.get_model('wagtailpages', 'GeneralProductPage')
    SoftwareProductPage = apps.get_model('wagtailpages', 'SoftwareProductPage')

    (DEFAULT_LOCALE, DEFAULT_LOCALE_ID) = get_default_locale()
    
    product_pages = [
        GeneralProductPage.objects.filter(locale_id=DEFAULT_LOCALE_ID),
        SoftwareProductPage.objects.filter(locale_id=DEFAULT_LOCALE_ID)
    ]
    
    for product_set in product_pages:
        update_fields_to_rich_text(product_set)



class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0051_auto_20211028_0220'),
    ]

    operations = [
        migrations.RunPython(
            code=gather_products_and_update_fields
        )
    ]
