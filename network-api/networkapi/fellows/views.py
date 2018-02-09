from django.shortcuts import render


# Create your views here.
def fellows_home(request):
    return render(request, 'fellows_home.html')


def fellows_science(request):
    return render(request, 'fellows_science.html')


def fellows_openweb(request):
    return render(request, 'fellows_openweb.html')


def fellows_directory(request):
    return render(request, 'fellows_directory.html')


def fellows_directory_senior(request):
    context = {'type': 'senior'}

    return render(request, 'fellows_directory_type.html', context)


def fellows_directory_science(request):
    context = {'type': 'science'}

    return render(request, 'fellows_directory_type.html', context)


def fellows_directory_open_web(request):
    context = {'type': 'open web'}

    return render(request, 'fellows_directory_type.html', context)


def fellows_directory_tech_policy(request):
    context = {'type': 'tech policy'}

    return render(request, 'fellows_directory_type.html', context)


def fellows_directory_media(request):
    context = {'type': 'media'}

    return render(request, 'fellows_directory_type.html', context)


def fellows_support(request):
    return render(request, 'fellows_support.html')


def fellows_apply(request):
    return render(request, 'fellows_apply.html')
