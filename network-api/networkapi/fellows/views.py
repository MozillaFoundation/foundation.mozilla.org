from django.conf import settings
from django.template.defaultfilters import slugify
from django.shortcuts import render
from django.http import Http404


# Create your views here.
def fellows_home(request):
    return render(request, 'fellows_home.html', {'pulse_domain': settings.FRONTEND['PULSE_DOMAIN']})


def fellows_type(request, program_type_slug):
    program_types = settings.FRONTEND['FELLOWSHIPS_PROGRAM_INFO_TYPES']

    if program_type_slug not in [slugify(item) for item in program_types]:
        raise Http404

    template = 'fellows_' + program_type_slug.replace('-', '_') + '.html'
    context = {'type': program_type_slug.replace('-', ' ')}

    return render(request, template, context)


def fellows_directory(request):
    return render(request, 'fellows_directory.html')


def fellows_directoy_type(request, program_type_slug):
    program_types = settings.FRONTEND['FELLOWSHIPS_DIRECTORY_TYPES']

    if program_type_slug not in [slugify(item) for item in program_types]:
        raise Http404

    program_type = program_type_slug.replace('-', ' ')
    context = {
        'type': program_type,
        'page_title': 'Fellows in Residence' if program_type == 'in residence' else program_type.title() + " Fellows"
    }

    return render(request, 'fellows_directory_type.html', context)


def fellows_support(request):
    return render(request, 'fellows_support.html')


def fellows_apply(request):
    return render(request, 'fellows_apply.html')
