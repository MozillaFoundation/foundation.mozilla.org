from django.conf import settings
from django.shortcuts import render
from django.http import Http404


# Create your views here.
def fellows_home(request):
    return render(request, 'fellows_home.html', {'pulse_domain': settings.FRONTEND['PULSE_DOMAIN']})


def fellows_type(request, program_type_slug):
    if program_type_slug not in ['science', 'open-web', 'tech-policy', 'media']:
        raise Http404

    template = 'fellows_' + program_type_slug.replace('-', '_') + '.html'
    context = {'type': program_type_slug.replace('-', ' ')}

    return render(request, template, context)


def fellows_directory(request):
    return render(request, 'fellows_directory.html')


def fellows_directory_previous_years(request):
    return render(request, 'fellows_directory_previous_years.html')


def fellows_support(request):
    return render(request, 'fellows_support.html')


def fellows_apply(request):
    return render(request, 'fellows_apply.html')
