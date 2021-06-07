import sys, traceback
from django.http import HttpResponse

def server_error_500_handler(request):
    type, value, tb = sys.exc_info()

    print('\n----intercepted 500 error stack trace----')
    print(value)
    print(type)
    print(traceback.format_exception(type, value, tb))
    print('----\n')

    return HttpResponse(status=404)
