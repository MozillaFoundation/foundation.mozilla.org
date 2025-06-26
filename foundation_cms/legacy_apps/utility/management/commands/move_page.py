import sys

from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page


class Command(BaseCommand):
    help = "Moves one or more pages (and their descendants) under a destination page."

    def render_progress_bar(self, current, total, bar_length=40):
        percent = current / total
        filled = int(bar_length * percent)
        bar = "▓" * filled + "░" * (bar_length - filled)
        sys.stdout.write(f"\rProgress: {bar} {int(percent * 100)}%")
        sys.stdout.flush()

    def handle(self, *args, **options):
        try:
            source_ids_input = input("Enter the IDs of the pages to move (comma-separated): ").strip()
            source_page_ids = [int(pid.strip()) for pid in source_ids_input.split(",") if pid.strip()]
            destination_page_id = int(input("Enter the ID of the destination parent page: ").strip())
        except ValueError:
            raise CommandError("All page IDs must be integers.")

        if destination_page_id in source_page_ids:
            raise CommandError("Destination page ID cannot be in the list of source page IDs.")

        try:
            destination_page = Page.objects.get(id=destination_page_id)
        except Page.DoesNotExist:
            raise CommandError(f"Destination page with ID {destination_page_id} does not exist.")

        pages_to_move = []

        for source_page_id in source_page_ids:
            try:
                source_page = Page.objects.get(id=source_page_id)
            except Page.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Page with ID {source_page_id} does not exist. Skipping."))
                continue

            if destination_page.is_descendant_of(source_page):
                self.stdout.write(
                    self.style.WARNING(f"Cannot move page {source_page_id} into one of its descendants. Skipping.")
                )
                continue

            pages_to_move.append(source_page)

        if not pages_to_move:
            self.stdout.write(self.style.WARNING("No valid pages to move. Exiting."))
            return

        print("\nThe following pages will be moved under " f"'{destination_page.title}' (ID {destination_page.id}):\n")
        for page in pages_to_move:
            print(f" • {page.title} (ID {page.id})")

        confirm = input("\nProceed with moving all of these pages? [y/N]: ").strip().lower()
        if confirm != "y":
            self.stdout.write(self.style.WARNING("Operation cancelled."))
            return

        total = len(pages_to_move)
        print("")  # space before progress bar

        for i, page in enumerate(pages_to_move, start=1):
            page.move(destination_page, pos="last-child")
            self.render_progress_bar(i, total)

        print()  # move to new line after progress bar

        self.stdout.write(self.style.SUCCESS("All pages moved successfully."))
