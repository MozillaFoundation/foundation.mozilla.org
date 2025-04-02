# Script to migrate usernames from Google's default firstname / firstname+lastnamecharacter to
# new default auth0 FirstnameLastname format. Normalize for special characters, and spaces, etc.

import unicodedata
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

def normalize_name(s):
    return (
        unicodedata.normalize('NFKD', s)
        .encode('ascii', 'ignore')
        .decode('ascii')
        .replace("-", "")
        .replace(" ", "")
    )

class Command(BaseCommand):
    help = "Migrate usernames to FirstnameLastname format"

    def handle(self, *args, **options):
        for user in User.objects.all():
            old_username = user.username
            if user.first_name and user.last_name:
                base = normalize_name(user.first_name).capitalize() + normalize_name(user.last_name).capitalize()
                username = base
                suffix = 1

                while User.objects.exclude(pk=user.pk).filter(username=username).exists():
                    username = f"{base}{suffix}"
                    suffix += 1

                user.username = username
                user.save()
                self.stdout.write(f"{old_username} → {user.username}")
            else:
                self.stdout.write(f"Skipped {old_username}: missing names")