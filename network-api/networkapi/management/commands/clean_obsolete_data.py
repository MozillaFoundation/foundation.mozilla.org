from django.db import transaction, connection
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    This command exists solely to clean up now-obsolete data due to squashing-and-rebuilding
    the mozfest and wagtailpages migrations, as well as deleting our obsolete buyersguide app.
    """

    content_type_id = "SELECT id FROM django_content_type WHERE app_label = 'buyersguide'"
    auth_permission_id = f"select id from auth_permission WHERE content_type_id in ({content_type_id})"
    statements = (
        "DELETE FROM django_migrations WHERE app = 'buyersguide'",
        f"DELETE FROM auth_group_permissions WHERE permission_id in ({auth_permission_id})",
        f"DELETE FROM auth_permission WHERE content_type_id in ({content_type_id})",
        "DELETE FROM django_content_type WHERE app_label = 'buyersguide'",
        "DELETE FROM django_migrations WHERE app = 'wagtailpages' AND id < 900",
        "DELETE FROM django_migrations WHERE app = 'mozfest' AND id < 904",
    )

    def handle(self, *args, **options):
        print("Running custom SQL")
        cursor = connection.cursor()
        for sql in self.statements:
            print(f"> {sql}")
            cursor.execute(sql)
        print("All SQL executed")
