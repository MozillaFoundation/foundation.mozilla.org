# # Generated by Django 3.0.14 on 2021-08-10 18:19

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.blocks.static_block
import wagtail.core.fields
import wagtail.images.blocks
import wagtailmedia.blocks


from networkapi.mozfest.models import MozfestPrimaryPage



def update_annotated_image_blocks(qs):
    # Loop through all pages
    for page in qs:
        print("\t", page)
        # If this page doesn't have a Image that needs update, don't save it.
        # This will speed up how fast this task can run.
        needs_saving = False
        # Only loop through streamfield data if there's a `body` field on the page
        if page.body:
            # Looping through raw_data is a List of blocks.
            for block in page.body.raw_data:
                # If there is a type in the blocks, and the block type is a image,
                # check if the image has the wide setting on
                if 'type' in block and block['type'] == "image":
                    # If so, set the new image_width value to wide
                    if 'wide_image' in block['value'] and block['value']['wide_image'] == True:
                        print("Found a wide image, updating.")
                        block['value']['image_width'] = "wide"
                        needs_saving = True

            if needs_saving:
                # If page is published already, continue to publish it.
                # Otherwise just save a revision for draft history.
                if page.live:
                    print("\t\tPage is live. Publish it")
                    page.save_revision().publish()
                else:
                    print("\t\tPage is draft.")
                    page.save_revision()

def loop_through_pages_with_image_blocks(apps, schema):
    # Only look through pages that ACTUALLY USE the Annotated Image Block streamfield.
    pages_with_image_blocks = [
        MozfestPrimaryPage.objects.all(),
    ]

    for page_qs in pages_with_image_blocks:
        print("Pages:", page_qs.count())
        if page_qs.count() != 0:
            update_annotated_image_blocks(page_qs)

class Migration(migrations.Migration):

    dependencies = [
        ('mozfest', '0016_add_image_width_select_field'),
    ]

    operations = [
                 migrations.RunPython(loop_through_pages_with_image_blocks)
    ]
