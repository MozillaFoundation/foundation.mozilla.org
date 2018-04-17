from wagtail_factories import (
    PageFactory,
    StreamFieldFactory,
)
from wagtail_factories.blocks import(
    BlockFactory,
    CharBlockFactory,
)
from factory import (
    Faker,
    Factory,
)
from wagtail.core import blocks
from networkapi.wagtailpages.models import OpportunityPage
from . import customblocks

class RichTextBlockFactory(BlockFactory):
    class Meta:
        model = blocks.RichTextBlock

class AlignedImageBlockFactory(BlockFactory):
    class Meta:
        model = customblocks.AlignedImageBlock

class FigureBlockFactory(BlockFactory):
    class Meta:
        model = customblocks.FigureBlock

class FigureGridBlockFactory(BlockFactory):
    class Meta:
        model = customblocks.FigureGridBlock

class VideoBlockFactory(BlockFactory):
    class Meta:
        model = customblocks.VideoBlock

class iFrameBlockFactory(BlockFactory):
    class Meta:
        model = customblocks.iFrameBlock

class LinkButtonBlockFactory(BlockFactory):
    class Meta:
        model = customblocks.LinkButtonBlock

class BootstrapSpacerBlockFactory(BlockFactory):
    class Meta:
        model = customblocks.BootstrapSpacerBlock

class OpportunityPageFactory(PageFactory):
    class Meta:
        model = OpportunityPage

    body = StreamFieldFactory({
        'heading': CharBlockFactory,
        'paragraph': RichTextBlockFactory,
        'image': AlignedImageBlockFactory,
    })

    header = Faker('text', max_nb_chars=50)
