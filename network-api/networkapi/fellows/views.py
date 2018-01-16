from django.shortcuts import render


# Create your views here.
def fellows_home(request):
    return render(request, 'fellows_home.html')
