from wagtail.blocks import CharBlock, ChoiceBlock, RegexBlock

from foundation_cms.base.models.base_block import BaseBlock


class SectionStartBlock(BaseBlock):
    """
    Marks the start of a page section in a flat StreamField.

    Every block after this marker, up to the next marker, is grouped into one
    section at render time (see `foundation_cms.blocks.sections`). Keeping the
    stream flat lets editors move blocks between sections with Wagtail's
    native reorder controls.
    """

    name = CharBlock(
        max_length=100,
        help_text="Labels this section in the CMS and its minimap. This is not shown on the page.",
    )
    # Maps to LP section/surface tokens, not the legacy background palette.
    surface = ChoiceBlock(
        choices=[
            ("default", "White (Default)"),
            ("ground", "Light grey (Ground)"),
        ],
        default="default",
        label="Background color",
    )
    # LP section master variants. Values are LP's variant names, which map to
    # the `mzf-c-section--*` modifier classes; LP's defaults (xlarge, large)
    # have no modifier class.
    rhythm = ChoiceBlock(
        choices=[
            ("large", "Compact (Large)"),
            ("xlarge", "Standard (XLarge)"),
            ("2xlarge", "Spacious (2XLarge)"),
        ],
        default="xlarge",
        label="Spacing between blocks",
    )
    padding = ChoiceBlock(
        choices=[
            ("large", "Standard (Large)"),
            ("small", "Compact (Small)"),
        ],
        default="large",
        label="Spacing above and below",
        help_text="Compact only applies on desktop. Both options are the same on mobile.",
    )
    anchor_id = RegexBlock(
        regex=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        required=False,
        max_length=50,
        error_messages={"invalid": "Use lowercase letters, numbers and hyphens only."},
        help_text="Optional ID for linking to this section, e.g. 'get-involved' for #get-involved.",
    )

    def render(self, value, context=None):
        # The grouping helper consumes markers before rendering, so this only
        # matters if the stream is rendered ungrouped: output nothing.
        return ""

    class Meta:
        # Dedicated icon: the admin CSS keys off it to group the minimap by section.
        icon = "section-marker"
        label = "Section Start"
        # Title the block by its name only. Without this, Wagtail falls back to
        # the first child with a value, so a new, unnamed marker is titled by
        # its background color in the block header and minimap.
        label_format = "{name}"
        form_classname = "section-start-block"
