from dataclasses import dataclass, field

SECTION_START_BLOCK_TYPE = "section_start"


@dataclass
class Section:
    """
    A run of stream blocks that share one section's settings.

    `settings` is the SectionStartBlock value that opened the section, or None
    for the implicit section holding any blocks before the first marker.
    """

    settings: object = None
    blocks: list = field(default_factory=list)

    @property
    def is_implicit(self):
        return self.settings is None


def group_into_sections(stream_value):
    """
    Split a flat StreamValue into sections at each `section_start` marker.

    - Blocks before the first marker form an implicit section (settings=None).
    - Markers with no blocks after them are dropped, so no empty sections render.
    - Block order is preserved and marker blocks are not included in `blocks`.
    """
    sections = []
    current = Section()

    for child in stream_value or []:
        # A marker closes the open section (kept only if it has blocks) and opens
        # a new one with the marker's settings. The marker itself isn't added.
        if child.block_type == SECTION_START_BLOCK_TYPE:
            if current.blocks:
                sections.append(current)
            current = Section(settings=child.value)
        # Any other block joins the open section.
        else:
            current.blocks.append(child)

    # The last open section is never closed by a marker, so keep it here,
    # unless it's empty because the page ends with a marker.
    if current.blocks:
        sections.append(current)

    return sections
