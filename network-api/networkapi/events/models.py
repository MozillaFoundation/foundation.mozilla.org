from django.db import models


class TitoEvent(models.Model):
    """
    Details of an event managed in Tito.

    Stores IDs and tokens associated with a specific event to be used when booking buttons are processed.
    """

    title = models.CharField(max_length=255)
    event_id = models.CharField(max_length=512, help_text='The ID of the event, e.g. "ultimateconf/2013"')
    security_token = models.CharField(max_length=255, help_text="Token used to sign webhooks for this event")
    newsletter_question_id = models.CharField(
        max_length=255,
        help_text="ID of the question in the Tito form that asks whether a user has opted in to receive newsletters",
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
