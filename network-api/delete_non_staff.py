"""Python script running with Heroku Scheduler add-on: check for accounts created by non-staff people and delete
them."""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "networkapi.settings")
django.setup()


def delete_non_staff():
    from django.contrib.auth.models import User, Group
    from django.db.models import Q

    print("Deleting non staff users")
    group_q = Group.objects.all()
    non_staff = User.objects.exclude(
        Q(email__contains='mozillafoundation.org') |
        Q(is_staff=True) |
        Q(groups__in=group_q)
    )

    if non_staff:
        print('Deleting: ')
        print(*[e.username for e in non_staff], sep=', ')
        non_staff.delete()
    else:
        print('Nothing to delete')
    print("Done!")


if __name__ == "__main__":
    delete_non_staff()
