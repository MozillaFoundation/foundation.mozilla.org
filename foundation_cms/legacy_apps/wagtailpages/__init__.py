from django.utils.translation import trans_real

from .override_utils import parse_accept_lang_header, to_language

# WARNING: this is not necessarily a good idea, but is the only way to override
# Django's default behaviour of requiring language codes to be lowercased.
# We have to modify the core Django method, because we have no way to replace
# all the core functionality that relies on this - e.g., url resolvers that
# the Django admin and third party apps use.
# A fix upstream has been asked in https://code.djangoproject.com/ticket/31795
# Replace some functions in django.utils.translation.trans_real with our own
# versions that support a language in the form en-US instead of en-us.
trans_real.to_language = to_language
trans_real.parse_accept_lang_header = parse_accept_lang_header
