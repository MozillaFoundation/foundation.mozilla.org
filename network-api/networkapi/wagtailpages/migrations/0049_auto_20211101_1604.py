# Generated by Django 3.1.11 on 2021-11-01 16:04
import itertools
import json
import uuid

from django.db import migrations


# Forward migration content handler
def update_body_to_use_single_quotes(content):
    needs_saving = False
    for index, block in enumerate(content):
        if "type" in block and block["type"] == "quote" and "quotes" in block["value"]:
            # Check if there is one StructBlock in the ListBlock (can theoretically be 0)
            if len(block["value"]["quotes"]):
                # Update the new block fields with the first quote from the old fields.
                single_quote = {
                    "type": "single_quote",
                    "value": {
                        "quote": block["value"]["quotes"][0]["quote"],
                        "attribution": block["value"]["quotes"][0]["attribution"],
                        "id": str(uuid.uuid4()),
                    },
                }
                content[index] = single_quote
                needs_saving = True

    return needs_saving, content


# Backward migration content handler
def update_body_to_use_quote_list(content):
    needs_saving = False
    for index, block in enumerate(content):
        # If there is a type in the blocks, and the block type is a quote
        # ListBlock Quotes are called "quote". Single quotes are called "callouts".
        # This namespacing is very helpful in this scenario.
        if "type" in block and block["type"] == "single_quote":
            quote_list_block = {
                "type": "quote",
                "value": {
                    "quotes": [
                        {
                            "quote": block["value"]["quote"],
                            "attribution": block["value"]["attribution"],
                        }
                    ]
                },
            }
            content[index] = quote_list_block
            needs_saving = True

    return needs_saving, content


def process(apps, func):
    PageRevision = apps.get_model("wagtailcore", "PageRevision")
    BlogPage = apps.get_model("wagtailpages", "BlogPage")
    ModularPage = apps.get_model("wagtailpages", "ModularPage")
    MozfestPrimaryPage = apps.get_model("mozfest", "MozfestPrimaryPage")
    PrimaryPage = apps.get_model("wagtailpages", "PrimaryPage")

    LOCALE_ID = 1

    pages = itertools.chain(
        BlogPage.objects.filter(locale_id=LOCALE_ID),
        ModularPage.objects.filter(locale_id=LOCALE_ID),
        MozfestPrimaryPage.objects.filter(locale_id=LOCALE_ID),
        PrimaryPage.objects.filter(locale_id=LOCALE_ID),
    )

    for page in pages:
        save_page, new_content = func(page.body.raw_data)
        if save_page:
            page.body.raw_data = new_content
            page.save()
            print(f"Saved page: {page.id}")

        for revision in PageRevision.objects.filter(page=page):
            revision_content = json.loads(revision.content_json)
            save_revision, new_content = func(json.loads(revision_content["body"]))
            if save_revision:
                revision_content["body"] = json.dumps(new_content)
                revision.content_json = json.dumps(revision_content)
                revision.save()
                print(f"Saved revision: {revision.id}")


def migrate_quote_list_blocks_to_single_quote_block(apps, schema):
    process(apps, update_body_to_use_single_quotes)


def migrate_single_quote_block_to_quote_list_blocks(apps, schema):
    process(apps, update_body_to_use_quote_list)


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0048_auto_20211101_1600"),
    ]

    operations = [
        migrations.RunPython(
            migrate_quote_list_blocks_to_single_quote_block,
            migrate_single_quote_block_to_quote_list_blocks,
        ),
    ]
