from django.conf import settings


# Used to export env variable to Django templates
def review_app(request):
    return {'HEROKU_APP_NAME': settings.HEROKU_APP_NAME}


# Used in BuyersGuide templates to check if we're using cloudinary
def cloudinary(request):
    return {'USE_CLOUDINARY': settings.USE_CLOUDINARY}
