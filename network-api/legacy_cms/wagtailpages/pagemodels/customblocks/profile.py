from wagtail import blocks
from wagtail.snippets import blocks as snippet_blocks

from legacy_cms.wagtailpages.pagemodels.profiles import Profile


class ProfileCard(blocks.StructBlock):
    profile = snippet_blocks.SnippetChooserBlock(Profile)


class ProfileBlock(blocks.StructBlock):
    profiles = blocks.ListBlock(ProfileCard(), min_num=1)

    class Meta:
        icon = "user"
        template = "wagtailpages/blocks/profile_block_rounded.html"
