from datetime import datetime
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.core.management.base import BaseCommand


def delete_non_staff():
    print("\nDeleting non staff users")
    group_q = Group.objects.all()
    non_staff = User.objects.exclude(
        Q(email__endswith='@mozillafoundation.org') |
        Q(is_staff=True) |
        Q(groups__in=group_q)
    )

    if non_staff:
        print('Deleting:', ', '.join([e.username for e in non_staff]))
        non_staff.delete()
    else:
        print('Nothing to delete')
    print("Done!")


class Command(BaseCommand):
    help = 'Command made to be used on Heroku: check for accounts created by non-staff and delete them. Run ' \
           'once per week on Sundays.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--now',
            action='store_true',
            dest='now',
            help="Execute this management command now."
        )

    def handle(self, *args, **options):

        if datetime.today().weekday() == 6:
            delete_non_staff()
        elif options['now']:
            delete_non_staff()
        else:
            print("Delete non-staff task only runs on Sundays. Skipping it.")
