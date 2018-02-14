from django.shortcuts import render


# Create your views here.
def fellows_home(request):
    return render(request, 'fellows_home.html')


def fellows_science(request):
    return render(request, 'fellows_science.html')


def fellows_openweb(request):
    return render(request, 'fellows_openweb.html')


def fellows_tech_policy(request):
    return render(request, 'fellows_tech_policy.html')


def fellows_media(request):
    return render(request, 'fellows_media.html')


def fellows_directory(request):
    return render(request, 'fellows_directory.html')


def fellows_directoy_type(request, program_type_slug):
    context = {'type': program_type_slug.replace('-', ' ')}

    return render(request, 'fellows_directory_type.html', context)


def fellows_support(request):
    return render(request, 'fellows_support.html')


def fellows_apply(request):
    return render(request, 'fellows_apply.html')
