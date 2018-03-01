from django.utils import timezone
from django.db import models
from django.db.models import Q
from adminsortable.models import SortableMixin

from networkapi.utility.images import get_image_upload_path
from wagtail.snippets.models import register_snippet


def get_people_image_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='people',
        prop_name='name',
        instance=instance,
        current_filename=filename
    )


def get_people_partnership_logo_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='people',
        prop_name='name',
        suffix='_partnership',
        instance=instance,
        current_filename=filename
    )


class PeopleQuerySet(models.query.QuerySet):
    """
    A QuerySet for people that filters for published people records
    """
    def published(self):
        now = timezone.now()

        queryset = self.filter(
            Q(expires__gt=now) | Q(expires__isnull=True),
            publish_after__lt=now
        )

        return queryset


class InternetHealthIssue(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


@register_snippet
class Person(SortableMixin):
    """
    A member of the Network
    """
    name = models.CharField(
        max_length=300,
        help_text='Person\'s Full Name',
    )
    role = models.CharField(
        max_length=300,
        help_text='Role within the Mozilla Network',
    )
    location = models.CharField(max_length=300)
    quote = models.TextField(
        max_length=1000,
        help_text='Quote about the awesomeness/impact of the network, '
                  'internet health or one of the issues',
        null=True,
        blank=True,
    )
    bio = models.TextField(
        max_length=5000,
        help_text='3 bullet-point biography of the person. Bullet-points '
                  'should use a \'-\' and each point should be on a new line',
        null=True,
        blank=True,
    )
    # We use FileField instead of ImageField since Django does not support
    # svgs for the ImageField
    image = models.FileField(
        max_length=2048,
        help_text='Profile image of the person',
        upload_to=get_people_image_upload_path
    )
    partnership_logo = models.FileField(
        max_length=2048,
        help_text='Affiliated Organization\'s logo',
        upload_to=get_people_partnership_logo_upload_path,
        null=True,
        blank=True,
    )
    twitter_url = models.URLField(
        max_length=2048,
        help_text='Link to twitter account',
        null=True,
        blank=True,
    )
    linkedin_url = models.URLField(
        max_length=2048,
        help_text='Link to LinkedIn account',
        null=True,
        blank=True,
    )
    interview_url = models.URLField(
        max_length=2048,
        help_text='Link to interview for featured people',
        null=True,
        blank=True
    )
    internet_health_issues = models.ManyToManyField(
        InternetHealthIssue,
        related_name='people',
        help_text='Which Internet Health Issues does the person most align '
                  'with?',
    )
    featured = models.BooleanField(
        help_text='Do you want to feature this person?',
        default=False,
    )
    publish_after = models.DateTimeField(
        help_text='Make this person\'s profile visible only after '
                  'this date and time (UTC)',
        null=True,
    )
    expires = models.DateTimeField(
        help_text='Hide this person\'s profile after this date and time (UTC)',
        default=None,
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True,
    )

    objects = PeopleQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'people'
        ordering = ('order',)

    def __str__(self):
        return str(self.name)


class Affiliation(models.Model):
    name = models.CharField(
        max_length=300,
        help_text='Organization\'s name',
    )
    person = models.ForeignKey(
        Person,
        related_name='affiliations',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)
