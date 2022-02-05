from wagtail.embeds import blocks


class DatawrapperBlock(blocks.EmbedBlock):

    class Meta:
        template = 'wagtailpages/blocks/datawrapper_block.html'
        help_text = (
            'Enter the "visualisation only" link of the Datawrapper embed. '
            'It looks something like this: https://datawrapper.dwcdn.net/KwSKp/1/'
        )
