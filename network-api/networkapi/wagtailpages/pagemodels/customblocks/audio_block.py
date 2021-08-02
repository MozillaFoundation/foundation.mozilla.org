from wagtail.core import blocks
from wagtailmedia.blocks import AbstractMediaChooserBlock
from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join



class AudioSelectorBlock(AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = '''
            <div>
                <video width="320" height="240" controls>
                    {0}
                    Your browser does not support the video tag.
                </video>
            </div>
            '''
        else:
            player_code = '''
            <div>
                <audio controls>
                    {0}
                    Your browser does not support the audio element.
                </audio>
            </div>
            '''

        return format_html(player_code, format_html_join(
            '\n', "<source{0}>",
            [[flatatt(s)] for s in value.sources]
        ))


class AudioBlock(blocks.StructBlock):

    audio = AbstractMediaChooserBlock()

    caption = blocks.CharBlock(
        required=False
    )

    class Meta:
        icon = 'media'
        template = 'wagtailpages/blocks/audio_block.html'
        # help_text = 'Design Guideline: Please crop images to a 16:6 aspect ratio when possible.'
