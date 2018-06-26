from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Check for accounts created by non-staff people and delete them'

    def handle(self, *args, **options):

        print("Deleting non staff users")
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
