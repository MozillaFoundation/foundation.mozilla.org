import json

from urllib import request
from django.conf import settings
from wagtail.core import blocks


class ProfileById(blocks.StructBlock):

    ids = blocks.CharBlock(
        label='Profile by ID',
        help_text='Show profiles for pulse users with specific profile ids'
                  ' (mozillapulse.org/profile/[##]). For multiple profiles'
                  ', specify a comma separated list (e.g. 85,105,332).'
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        ids = context['block'].value['ids'].replace(' ', '')
        profiles = list()

        # FIXME: the protocol should be part of the pulse api variable.
        #   see: https://github.com/mozilla/foundation.mozilla.org/issues/1824

        url = "{pulse_api}/api/pulse/v2/profiles/?format=json&ids={ids}".format(
            pulse_api=settings.FRONTEND['PULSE_API_DOMAIN'],
            ids=ids
        )

        try:
            response = request.urlopen(url)
            response_data = response.read()
            data = json.loads(response_data)

            as_dict = {}
            for profile in data:
                as_dict[str(profile['profile_id'])] = profile

            profiles = [as_dict[id] for id in ids.split(',')]

        except (IOError, ValueError) as exception:
            print(str(exception))
            pass

        context['profiles'] = profiles
        return context

    class Meta:
        template = 'wagtailpages/blocks/profile_blocks.html'
        icon = 'user'
