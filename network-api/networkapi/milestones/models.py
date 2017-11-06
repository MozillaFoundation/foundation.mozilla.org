from django.db import models

from networkapi.utility.images import get_image_upload_path


def get_milestone_photo_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='milestones',
        prop_name='headline',
        instance=instance,
        current_filename=filename
    )


class Milestone(models.Model):
    headline = models.CharField(
        max_length=300,
        help_text='Title of the milestone'
    )
    photo = models.FileField(
        max_length=2048,
        help_text='Image associated with the milestone',
        upload_to=get_milestone_photo_upload_path,
    )
    start_date = models.DateField(
        help_text='Date on which the milestone begins'
    )
    end_date = models.DateField(
        help_text='Date on which the milestone ends'
    )
    description = models.TextField(
        help_text='Briefly describe what the milestone '
                  'is all about',
    )
    link_url = models.URLField(
        max_length=500,
        help_text='URL link to the milestone',
    )
    link_label = models.CharField(
        max_length=300,
        help_text='Text to describe the milestone link'
    )

    class Meta:
        verbose_name_plural = 'milestones'
        ordering = ('start_date',)

    def __str__(self):
        return str(self.headline)
