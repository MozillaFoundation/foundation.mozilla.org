from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class MissingMigrationsTests(TestCase):
    def test_no_migrations_missing(self):
        """
        Ensure we didn't forget a migration
        """
        output = StringIO()
        call_command("makemigrations", interactive=False, dry_run=True, stdout=output)

        if output.getvalue() != "No changes detected\n":
            raise AssertionError("Missing migrations detected:\n" + output.getvalue())
