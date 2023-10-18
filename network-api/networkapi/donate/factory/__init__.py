from . import help_page, landing_page


def generate(seed):
    # these are not, and should not be, alphabetically ordered.
    landing_page.generate(seed)
    help_page.generate(seed)


__all__ = [
    "generate",
]
