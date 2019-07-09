from django.http import HttpResponseNotFound
from django.shortcuts import render


def custom404_view(request, exception):
    if request.site.hostname == 'mozillafestival.org':
        html = render(request, 'mozfest/404.html')
        return HttpResponseNotFound(html)
    else:
        html = render(request, '404.html')
        return HttpResponseNotFound(html)
