from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import Http404

from networkapi.homepage.models import Homepage
from networkapi.homepage.serializers import HomepageSerializer


class HomepageView(APIView):
    """
    A view that permits a GET to receive the related models on the homepage
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        homepage = Homepage.objects.last()

        if homepage is None:
            raise Http404('Homepage has not been created yet')

        serializer = HomepageSerializer(homepage, context={'request': request})
        return Response(serializer.data)
