import math

from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from .tabbed_content_tab_block import TabbedContentTabBlock


class TabbedContentContainerBlock(BaseBlock):
    CARDS_PER_PAGE = 4

    tabs = blocks.ListBlock(TabbedContentTabBlock(), min_num=1, max_num=8, label="Tabs")

    class Meta:
        template_name = "tabbed_content_container_block.html"
        icon = "folder-open-1"
        label = "Tabbed Content"

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)
        ctx["cards_per_page"] = self.CARDS_PER_PAGE
        ctx["tabs_with_page_counts"] = [
            (
                tab,
                math.ceil(
                    sum(1 for b in tab["content"] if b.block_type == "tab_card_set")
                    / self.CARDS_PER_PAGE
                ),
            )
            for tab in value["tabs"]
        ]
        return ctx
