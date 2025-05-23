from wagtail import blocks
from foundation_cms.base.models.base_block import BaseBlock
from .tabbed_content_tab_block import TabbedContentTabBlock


class TabbedContentContainerBlock(BaseBlock):
    tabs = blocks.ListBlock(
        TabbedContentTabBlock(),
        min_num=1,
        max_num=8,
        label="Tabs"
    )

    class Meta:
        template_name = "tabbed_content_container_block.html"
        icon = "folder-open-1"
        label = "Tabbed Content"