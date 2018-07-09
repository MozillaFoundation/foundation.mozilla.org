from django.conf import settings


# Used to export env variable to Django templates
def review_app(request):
    return {'HEROKU_APP_NAME': settings.HEROKU_APP_NAME}
