from django.db import migrations

LEGACY_GROUP_NAME = "access/legacy content editor"
DEFAULT_GROUP_NAME = "access/content editor: no publishing access"
SNIPPET_EDITORS_GROUP_NAME = "Snippet Editors"

# All legacy app labels whose model permissions should be gated behind the legacy group.
# Mozfest is intentionally included here for snippets, even though mozfest pages are
# managed via the CMS page tree rather than code-level restrictions.
LEGACY_APP_LABELS = [
    "campaign",
    "donate",
    "donate_banner",
    "events",
    "highlights",
    "mozfest",
    "nav",
    "news",
    "people",
    "wagtailpages",
]


def create_legacy_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    legacy_group, _ = Group.objects.get_or_create(name=LEGACY_GROUP_NAME)

    legacy_permissions = Permission.objects.filter(content_type__app_label__in=LEGACY_APP_LABELS)
    legacy_group.permissions.set(legacy_permissions)

    # Remove legacy permissions from the default content editor and snippet editor groups
    # so that only members of the legacy group (and superusers) can access legacy content.
    for group_name in (DEFAULT_GROUP_NAME, SNIPPET_EDITORS_GROUP_NAME):
        try:
            group = Group.objects.get(name=group_name)
            group.permissions.remove(*legacy_permissions)
        except Group.DoesNotExist:
            pass


def delete_legacy_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    Group.objects.filter(name=LEGACY_GROUP_NAME).delete()

    # Restore legacy permissions to the default content editor and snippet editor groups
    # so they are left in the same state as before this migration ran.
    legacy_permissions = Permission.objects.filter(content_type__app_label__in=LEGACY_APP_LABELS)
    for group_name in (DEFAULT_GROUP_NAME, SNIPPET_EDITORS_GROUP_NAME):
        try:
            group = Group.objects.get(name=group_name)
            group.permissions.add(*legacy_permissions)
        except Group.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0173_add_legacy_to_verbose_names"),
    ]

    operations = [
        migrations.RunPython(create_legacy_group, reverse_code=delete_legacy_group),
    ]
