from wagtail import blocks


class PulseProjectQueryValue(blocks.StructValue):
    @property
    def size(self):
        max_number_of_results = self["max_number_of_results"]
        return "" if max_number_of_results <= 0 else max_number_of_results

    @property
    def rev(self):
        # The default API behaviour is newest-first, so the "rev" attribute
        # should only have an attribute value when oldest-first is needed.
        newest_first = self["newest_first"]
        return True if newest_first else ""


class PulseProjectList(blocks.StructBlock):
    search_terms = blocks.CharBlock(
        help_text="Test your search at https://api.mozillapulse.org/api/pulse/v2/entries/ (e.g., https://api.mozillapulse.org/api/pulse/v2/entries/?search=mozfest)",
        label="Search",
        required=False,
    )

    max_number_of_results = blocks.IntegerBlock(
        min_value=0,
        max_value=12,
        default=6,
        required=True,
        help_text="Choose 1-12. If you want visitors to see more, link to a search or tag on Pulse.",
    )

    only_featured_entries = blocks.BooleanBlock(
        default=False,
        label="Display only featured entries",
        help_text="Featured items are selected by Pulse moderators.",
        required=False,
    )

    newest_first = blocks.ChoiceBlock(
        choices=[
            ("True", "Show newer entries first"),
            ("False", "Show older entries first"),
        ],
        required=True,
        label="Sort",
        default="True",
    )

    advanced_filter_header = blocks.StaticBlock(
        label=" ",
        admin_text="-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------",
    )

    issues = blocks.ChoiceBlock(
        choices=[
            ("all", "All"),
            ("Decentralization", "Decentralization"),
            ("Digital Inclusion", "Digital Inclusion"),
            ("Online Privacy & Security", "Online Privacy & Security"),
            ("Open Innovation", "Open Innovation"),
            ("Web Literacy", "Web Literacy"),
        ],
        required=True,
        default="all",
    )

    help = blocks.ChoiceBlock(
        choices=[
            ("all", "All"),
            ("Attend", "Attend"),
            ("Create content", "Create content"),
            ("Code", "Code"),
            ("Design", "Design"),
            ("Fundraise", "Fundraise"),
            ("Join community", "Join community"),
            ("Localize & translate", "Localize & translate"),
            ("Mentor", "Mentor"),
            ("Plan & organize", "Plan & organize"),
            ("Promote", "Promote"),
            ("Take action", "Take action"),
            ("Test & feedback", "Test & feedback"),
            ("Write documentation", "Write documentation"),
        ],
        required=True,
        default="all",
        label="Type of help needed",
    )

    class Meta:
        template = "wagtailpages/blocks/pulse_project_list.html"
        icon = "site"
        value_class = PulseProjectQueryValue
