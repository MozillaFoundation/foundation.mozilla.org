from datetime import tzinfo, timedelta

ZERO = timedelta(0)


class UTC(tzinfo):
    """UTC time"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO
