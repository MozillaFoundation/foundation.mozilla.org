from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = (
        "Pre-creates one fully-migrated test database per pytest-xdist worker, cloned "
        "from a single migrated template via Postgres `CREATE DATABASE ... TEMPLATE`. "
        "Run this before `pytest --reuse-db -n <worker_count>` so pytest-django finds "
        "each worker's database already migrated instead of replaying the full "
        "migration history once per worker, which otherwise dominates CI wall-clock "
        "time as more xdist workers or shards are added."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "worker_count",
            type=int,
            help="Number of pytest-xdist workers (must match -n passed to pytest).",
        )

    def handle(self, *args, **options):
        worker_count = options["worker_count"]
        if worker_count < 1:
            raise CommandError("worker_count must be at least 1")

        for alias in connections.databases:
            connection = connections[alias]
            if connection.settings_dict["ENGINE"] != "django.db.backends.postgresql":
                self.stdout.write(f"Skipping non-Postgres alias '{alias}'")
                continue

            base_name = connection.settings_dict["NAME"]
            test_base_name = f"test_{base_name}"
            template_name = f"{test_base_name}_template"

            self._create_database(connection, template_name)
            self._migrate_database(connection, alias, template_name)

            for worker_index in range(worker_count):
                worker_db_name = f"{test_base_name}_gw{worker_index}"
                self._create_database(connection, worker_db_name, template=template_name)
                self.stdout.write(f"Cloned {worker_db_name} from {template_name}")

    def _create_database(self, connection, db_name, template=None):
        with connection.cursor() as cursor:
            cursor.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
            if template:
                cursor.execute(f'CREATE DATABASE "{db_name}" TEMPLATE "{template}"')
            else:
                cursor.execute(f'CREATE DATABASE "{db_name}"')

    def _migrate_database(self, connection, alias, db_name):
        # Mirrors Django's own test-db setup (see create_test_db in
        # django/db/backends/base/creation.py): repoint this alias at the target
        # database and close the connection so the next query opens a fresh one there.
        original_name = connection.settings_dict["NAME"]
        connection.close()
        connection.settings_dict["NAME"] = db_name
        try:
            call_command("migrate", verbosity=1, interactive=False, database=alias, run_syncdb=True)
        finally:
            connection.close()
            connection.settings_dict["NAME"] = original_name
