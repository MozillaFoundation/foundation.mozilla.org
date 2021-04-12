from django.core.management.base import BaseCommand
from taggit.models import Tag


class Command(BaseCommand):
    help = '''
        Remove unused tags, if there are any. Then look for similar tags and delete the duplicates.
        The remaining tag will be renamed to a lowercase tag in preparation for case insensitive
        tags.
    '''

    def handle(self, *args, **options):
        for tag in Tag.objects.all():
            if (
                not tag.wagtailpages_blogpagetag_items.all()
                and not tag.wagtailpages_banneredcampaigntag_items.count()
            ):
                # This tag is not being used. Deleted it.
                tag.delete()
            else:
                # Tag is being used. Look for other tags with the same name and remove them.
                Tag.objects.filter(name__iexact=tag.name).exclude(slug=tag.slug)

                # Make the tag in the forloop have a lowercase name
                tag.name = tag.name.lower()
                tag.save()
