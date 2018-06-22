from django.contrib.auth.models import User
from django.db.models import Q


def delete_non_staff():
    print("Deleting non staff users")
    non_staff = User.objects.exclude(Q(email__contains='mozillafoundation,org') | Q(is_staff=True))
    for e in non_staff:
        print(f'Deleting {e.username}')
        e.delete()
    print("Done!")
