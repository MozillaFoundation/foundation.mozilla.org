from django.contrib.auth.models import User
from django.db.models import Q


def delete_non_staff():
    print("Deleting non staff users")
    User.objects.exclude(Q(email__contains='mozillafoundation,org') | Q(is_staff=True)).delete()
    print("Done!")
