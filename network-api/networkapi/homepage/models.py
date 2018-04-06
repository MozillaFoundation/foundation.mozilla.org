from django.db import models
from mezzanine.core.models import Orderable

from networkapi.people.models import Person
from networkapi.news.models import News
from networkapi.highlights.models import Highlight


# The old homepage
class Homepage(models.Model):
    class Meta:
        verbose_name_plural = 'homepage'


class HomepageLeaders(Orderable):
    leader = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='leaders_related_homepage',
    )
    homepage = models.ForeignKey(
        Homepage,
        on_delete=models.CASCADE,
        related_name='homepage_related_leaders',
    )

    class Meta:
        verbose_name = 'featured network leader'
        verbose_name_plural = 'network leaders (People)'


class HomepageNews(Orderable):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='news_related_homepage',
    )
    homepage = models.ForeignKey(
        Homepage,
        on_delete=models.CASCADE,
        related_name='homepage_related_news',
    )

    class Meta:
        verbose_name = 'featured news item'
        verbose_name_plural = 'latest from the network (News)'


class HomepageHighlights(Orderable):
    highlights = models.ForeignKey(
        Highlight,
        on_delete=models.CASCADE,
        related_name='highlights_related_homepage',
    )
    homepage = models.ForeignKey(
        Homepage,
        on_delete=models.CASCADE,
        related_name='homepage_related_highlights',
    )

    class Meta:
        verbose_name = 'featured highlight'
        verbose_name_plural = 'get involved (Highlights)'
