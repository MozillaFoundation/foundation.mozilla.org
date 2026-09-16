from django.db import migrations


def delete_orphaned_buyersguide_pages(apps, schema_editor):
    """
    0178 dropped the buyersguide page models but never deleted the
    corresponding wagtailcore_page rows. Any page left with a content_type
    pointing at one of these now-nonexistent models breaks Wagtail admin
    actions (draft/publish/preview, the explorer side panel) that resolve
    .specific on the page or its revisions, since ContentType.model_class()
    returns None for a deleted model.

    Queries the base Page model directly (never .specific) so this is safe
    to run even where the orphan already exists. A no-op anywhere already
    clean, including a fresh migrate from zero.
    """
    ContentType = apps.get_model("contenttypes", "ContentType")
    Page = apps.get_model("wagtailcore", "Page")

    orphaned_model_names = [
        "buyersguidepage",
        "buyersguidearticlepage",
        "buyersguidecampaignpage",
        "consumercreepometerpage",
        "buyersguideeditorialcontentindexpage",
        "productpage",
        "generalproductpage",
    ]
    content_types = ContentType.objects.filter(app_label="wagtailpages", model__in=orphaned_model_names)
    Page.objects.filter(content_type__in=content_types).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailpages", "0179_remove_articlepage_show_side_share_buttons"),
    ]

    operations = [
        migrations.RunPython(delete_orphaned_buyersguide_pages, migrations.RunPython.noop),
    ]
