from wagtail import blocks


class ResearcherRoleBlock(blocks.StructBlock):
    """
    Block for the Researcher role with specific fields.
    """

    research_area = blocks.CharBlock(help_text="Research area or expertise")
    institution = blocks.CharBlock(help_text="Affiliated institution")

    class Meta:
        label = "Researcher Role"
        icon = "user"  # Wagtail admin icon
        template = "profiles/blocks/researcher_role_block.html"


class BlogAuthorRoleBlock(blocks.StructBlock):
    """
    Block for the Blog Author role with specific fields.
    """

    blog_topic = blocks.CharBlock(help_text="Primary blog topic or category")
    bio = blocks.TextBlock(help_text="Short author bio")

    class Meta:
        label = "Blog Author Role"
        icon = "edit"
        template = "profiles/blocks/blog_author_role_block.html"


class GranteeRoleBlock(blocks.StructBlock):
    """
    Block for the Grantee role with specific fields.
    """

    project = blocks.CharBlock(help_text="Primary project")

    class Meta:
        label = "Grantee Role"
        icon = "edit"
        template = "profiles/blocks/blog_author_role_block.html"
