"""Python script running with Heroku Scheduler add-on: check for accounts created by non-staff people and delete
them."""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "networkapi.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from django.db.models import Q  # noqa: E402

print("Deleting non staff users")
non_staff = User.objects.exclude(Q(email__contains='mozillafoundation,org') | Q(is_staff=True))
if non_staff:
    print('Deleting: ')
    print(*[e.username for e in non_staff], sep=', ')
    non_staff.delete()
else:
    print('Nothing to delete')
print("Done!")
