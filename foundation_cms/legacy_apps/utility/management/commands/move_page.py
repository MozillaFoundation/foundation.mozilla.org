from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page


class Command(BaseCommand):
    help = "Interactively moves a page and all its descendants under a new parent page."

    def handle(self, *args, **options):
        try:
            source_page_id = int(input("Enter the ID of the page you want to move: ").strip())
            destination_page_id = int(input("Enter the ID of the destination parent page: ").strip())
        except ValueError:
            raise CommandError("Both page IDs must be integers.")

        if source_page_id == destination_page_id:
            raise CommandError("Source and destination pages must be different.")

        try:
            source_page = Page.objects.get(id=source_page_id)
        except Page.DoesNotExist:
            raise CommandError(f"Source page with ID {source_page_id} does not exist.")

        try:
            destination_page = Page.objects.get(id=destination_page_id)
        except Page.DoesNotExist:
            raise CommandError(f"Destination page with ID {destination_page_id} does not exist.")

        if destination_page.is_descendant_of(source_page):
            raise CommandError("Cannot move a page into one of its own descendants.")

        confirm = (
            input(
                f"Move page '{source_page.title}' (ID {source_page.id}) "
                f"under '{destination_page.title}' (ID {destination_page.id})? [y/N]: "
            )
            .strip()
            .lower()
        )

        if confirm != "y":
            self.stdout.write("Operation cancelled.")
            return

        source_page.move(destination_page, pos="last-child")

        self.stdout.write(
            self.style.SUCCESS(
                f"Page {source_page.id} and its children were successfully moved under page {destination_page.id}."
            )
        )