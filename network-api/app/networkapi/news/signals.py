from django.db.models.signals import post_save, post_delete

from networkapi.utility.build import build_static_site
from networkapi.news.models import News


def setup_signals():
    post_save.connect(build_static_site, sender=News)
    post_delete.connect(build_static_site, sender=News)
