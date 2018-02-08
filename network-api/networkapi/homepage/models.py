from django.db import models
from mezzanine.core.models import Orderable

from networkapi.people.models import Person
from networkapi.news.models import News
from networkapi.highlights.models import Highlight
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Orderable as WagtailOrderable
from wagtail.wagtailadmin.edit_handlers import InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel


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


# Code for the new wagtail based homepage

class HomepageRelatedPeople(WagtailOrderable, Person):
    page = ParentalKey(
        'WagtailHomePage',
        related_name='homepage_people',
    )
    people = models.ForeignKey(Person, related_name='homepage_people')
    panels = [
        SnippetChooserPanel('people'),
    ]


class HomepageRelatedNews(WagtailOrderable, News):
    page = ParentalKey(
        'WagtailHomePage',
        related_name='homepage_news',
    )
    news = models.ForeignKey(News, related_name='homepage_news')
    panels = [
        SnippetChooserPanel('news'),
    ]


class HomepageRelatedHighlights(WagtailOrderable, Highlight):
    page = ParentalKey(
        'WagtailHomePage',
        related_name='homepage_highlights',
    )
    highlights = models.ForeignKey(Highlight, related_name='homepage_highlights')
    panels = [
        SnippetChooserPanel('highlights'),
    ]


class WagtailHomepage(Page):

    content_panels = Page.content_panels + [
      InlinePanel('homepage_people', label="People", max_num=3),
      InlinePanel('homepage_news', label="News", max_num=3),
      InlinePanel('homepage_highlights', label="Highlights", max_num=3),
    ]
