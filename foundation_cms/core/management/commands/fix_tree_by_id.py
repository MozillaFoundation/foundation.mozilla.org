from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page


class Command(BaseCommand):
    help = "Fix tree structure for a specific page ID"

    def add_arguments(self, parser):
        parser.add_argument("page_id", type=int, help="Page ID to fix tree for")

    def handle(self, *args, **options):
        page_id = options["page_id"]

        try:
            page = Page.objects.get(id=page_id)
            print(f"Fixing tree for: {page.title} (ID: {page_id})")

            # Count before
            children_before = page.get_children().count()
            print(f"Children before: {children_before}")

            page.fix_tree()

            # Count after
            page.refresh_from_db()
            children_after = page.get_children().count()
            print(f"Children after: {children_after}")

            print("Done")

        except Page.DoesNotExist:
            raise CommandError(f"Page with ID {page_id} not found")
