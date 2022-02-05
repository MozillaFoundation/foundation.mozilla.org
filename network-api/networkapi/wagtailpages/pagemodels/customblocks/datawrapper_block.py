from wagtail.embeds import blocks


class DatawrapperBlock(blocks.EmbedBlock):
    class Meta:
        template = 'wagtailpages/blocks/datawrapper_block.html'
