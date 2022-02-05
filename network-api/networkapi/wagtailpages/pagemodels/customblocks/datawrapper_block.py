from django.core.exceptions import ValidationError
from wagtail.embeds import blocks


class DatawrapperBlock(blocks.EmbedBlock):
    class Meta:
        template = 'wagtailpages/blocks/datawrapper_block.html'
        help_text = (
            'Enter the "visualisation only" link of the Datawrapper embed. '
            'It looks something like this: https://datawrapper.dwcdn.net/KwSKp/1/'
        )

    def clean(self, value):
        # TODO: Replace this naive check with something based on the regex
        if isinstance(value, blocks.EmbedValue) and not "datawrapper" in value.url.lower():
            raise ValidationError("Please enter a Datawrapper URL.")
        return super().clean(value)
