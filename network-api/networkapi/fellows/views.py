from django.shortcuts import render


# Create your views here.
def fellows_home(request):
    print('Rendering Fellows Home')
    return render(request, 'fellows_home.html')


def fellows_directory(request):
    return render(request, 'fellows_directory.html')


def fellows_support(request):
    return render(request, 'fellows_support.html')


def fellows_science(request):
    return render(request, 'fellows_science.html')


def fellows_openweb(request):
    return render(request, 'fellows_openweb.html')
