from django.views import View
from django.shortcuts import render


class FellowHomeView(View):

  def get(self, request):
      return render(request, 'fellows_home.html')


class FellowDirectoryView(View):

  def get(self, request):
      return render(request, 'fellows_directory.html')


class FellowSupportView(View):

  def get(self, request):
      return render(request, 'fellows_support.html')


class FellowScienceView(View):

  def get(self, request):
      return render(request, 'fellows_science.html')


class FellowOpenWebView(View):

  def get(self, request):
      return render(request, 'fellows_openweb.html')
