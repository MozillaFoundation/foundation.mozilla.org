from . import BaseCardBlock


class PillarCardBlock(BaseCardBlock):
    label = None
    image = None

    class Meta:
        label = "Pillar Card"
        icon = "form"
