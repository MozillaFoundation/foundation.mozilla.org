from networkapi.wagtailpages.models import Signup
from .abstract import CTAFactory


class SignupFactory(CTAFactory):
    class Meta:
        model = Signup
