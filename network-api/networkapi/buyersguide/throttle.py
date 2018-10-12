from rest_framework.throttling import UserRateThrottle
from django.conf import settings


# custom User rate class that overrides the default rate limit for UserRateThrottle
class UserVoteRateThrottle(UserRateThrottle):
    rate = settings.BUYERS_GUIDE_VOTE_RATE_LIMIT


# class to use in testing to bypass rate limiting
class TestUserVoteRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        # returning `None` means the request should not be throttled
        return None
