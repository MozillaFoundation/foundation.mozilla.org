from wagtail.blocks import BooleanBlock, PageChooserBlock

from foundation_cms.base.models.base_block import BaseBlock


class ProjectBlock(BaseBlock):
    """
    Displays one Gallery Hub Project Page as a reusable project card.
    """

    project = PageChooserBlock(
        required=True,
        page_type="gallery_hub.ProjectPage",
        label="Project",
    )
    show_description = BooleanBlock(
        required=False,
        default=True,
        label="Show description",
    )

    class Meta:
        label = "Project Block"
        icon = "image"
        template_name = "project_block.html"
