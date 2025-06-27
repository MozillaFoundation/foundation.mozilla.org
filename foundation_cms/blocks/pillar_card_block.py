from . import BaseCardBlock


class PillarCardBlock(BaseCardBlock):
    label = None
    # TODO:FIXME: remove image field

    class Meta:
        label = "Pillar Card"
        icon = "form"
