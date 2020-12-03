from django.db import connection
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Removes the milestones app - use post-deploy'

    def handle(self, *args, **options):
        DEL_APPS = ['milestones']
        contentTypes = ContentType.objects.all().order_by('app_label', 'model')
        for entry in contentTypes:
            if (entry.app_label in DEL_APPS):
                print(f'Deleting Content Type {entry.app_label} {entry.model}')
                entry.delete()

        with connection.cursor() as cursor:
            cursor.execute("DROP SEQUENCE IF EXISTS milestones_milestone_id_seq CASCADE")
            cursor.execute("DROP TABLE IF EXISTS milestones_milestone CASCADE")
