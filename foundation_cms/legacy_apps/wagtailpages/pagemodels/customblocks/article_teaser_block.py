from wagtail import blocks


class ArticleTeaserCard(blocks.StructBlock):
    article = blocks.PageChooserBlock(
        required=False,
        help_text="Page that this should link out to.",
        target_model="wagtailpages.ArticlePage",
    )


class ArticleTeaserBlock(blocks.StructBlock):
    cards = blocks.ListBlock(ArticleTeaserCard(), help_text="Please use a minimum of 3 cards.", min_num=3)

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/article_teaser_block.html"
