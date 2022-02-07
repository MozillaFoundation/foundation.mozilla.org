from wagtail.embeds import blocks


class DatawrapperBlock(blocks.EmbedBlock):
    """
    Embed block for Datawrapper visualisations.

    Currently, there is no limitation in the block itself on which oEmbed sources
    it can be used with. The available oEmbed source are limited in the settings
    and currently only includes Datawrapper.

    The block type mainly exists to provide a consistent help text to the editors.
    The help text should support editors in fining the correct URL in the Datawrapper
    dashboard.

    The current implementation of the block simply inserts the HTML from Datawrappers
    oEmbed response into the template. The response from Datawrapper includes the
    `iframe` element and a small `script` tag. The JS only adds some additional
    reponsiveness features to the embed. If multiple embeds are used on the same page
    then the same `script` tag will be included multiple times on the page. This should
    not be much of an issue but only increase the length of the document a bit. If the
    repetition is considered an issue in the future, it should be possible to use the
    `options` settings for the Datawrapper oEmbed finder to modify the request so that
    the reponse only contains the `iframe`.

    See also:
    - https://docs.wagtail.org/en/stable/advanced_topics/embeds.html#customising-an-individual-provider
    - https://developer.datawrapper.de/docs/embedding-charts-via-oembed

    """
    _default_help_text = (
        'Enter the "visualisation only" link of the Datawrapper chart. '
        'It looks something like this: https://datawrapper.dwcdn.net/KwSKp/1/'
    )

    def __init__(self, *args, **kwargs):
        # Help text is set in the constructor rather than the `Meta` class to work
        # around a bug in Wagtail: https://github.com/wagtail/wagtail/issues/7929
        help_text = kwargs.get("help_text", self._default_help_text)
        kwargs["help_text"] = help_text
        return super().__init__(*args, **kwargs)

    def deconstruct(self):
        """
        Custom deconstruct method to define class representation in migrations.

        This is necessary to prevent issue with migrations when the class is moved.

        See also:
        https://docs.wagtail.org/en/stable/advanced_topics/customisation/streamfield_blocks.html#handling-block-definitions-within-migrations

        """
        path = 'wagtail.embeds.blocks.EmbedBlock'
        args = []
        kwargs = {
            "icon": self.meta.icon,
            "template": self.meta.template,
            "help_text": self._default_help_text,
        }
        return path, args, kwargs


    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/datawrapper_block.html'
