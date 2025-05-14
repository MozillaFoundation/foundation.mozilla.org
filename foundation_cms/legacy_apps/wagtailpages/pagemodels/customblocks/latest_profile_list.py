import json
from urllib import parse, request

from django.conf import settings
from wagtail import blocks


class LatestProfileQueryValue(blocks.StructValue):
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


class LatestProfileList(blocks.StructBlock):
    max_number_of_results = blocks.IntegerBlock(
        min_value=1,
        max_value=48,
        default=12,
        required=True,
        help_text="Pick up to 48 profiles.",
    )

    advanced_filter_header = blocks.StaticBlock(
        label=" ",
        admin_text="-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------",
    )

    profile_type = blocks.CharBlock(required=False, default="", help_text="Example: Fellow.")

    program_type = blocks.CharBlock(required=False, default="", help_text="Example: Tech Policy.")

    year = blocks.CharBlock(required=False, default="")

    def get_context(
        self,
        value,
        parent_context=None,
        no_limit=False,
        initial_year=False,
        ordering=False,
    ):
        context = super().get_context(value, parent_context=parent_context)

        query_args = {
            "limit": value["max_number_of_results"],
            "profile_type": value["profile_type"],
            "program_type": value["program_type"],
            "program_year": initial_year if initial_year else value["year"],
            "ordering": ordering if ordering else "-id",
            "is_active": "true",
            "format": "json",
        }

        # Removing after the fact is actually easier than
        # conditionally adding and then filtering the list.
        if no_limit:
            query_args.pop("limit")

        # Filter out emptish values
        query_args = {k: v for k, v in query_args.items() if v}

        url = "{pulse_api}/api/pulse/v2/profiles/?{query}".format(
            pulse_api=settings.FRONTEND["PULSE_API_DOMAIN"],
            query=parse.urlencode(query_args),
        )

        data = []

        try:
            response = request.urlopen(url)
            response_data = response.read()
            data = json.loads(response_data)

            for profile in data:
                profile["created_entries"] = False
                profile["published_entries"] = False
                profile["entry_count"] = False
                profile["user_bio_long"] = False

        except (OSError, ValueError) as exception:
            print(str(exception))
            pass

        context["profiles"] = data
        context["profile_type"] = value["profile_type"]
        context["program_type"] = value["program_type"]
        context["program_year"] = value["year"]
        return context

    class Meta:
        template = "wagtailpages/blocks/profile_blocks.html"
        icon = "group"
        value_class = LatestProfileQueryValue
