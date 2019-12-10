from django.conf import settings


# Used to export env variable to Django templates
def review_app(request):
    return {'REVIEW_APP': settings.REVIEW_APP}


# Used in BuyersGuide templates to check if we're using cloudinary
def cloudinary(request):
    return {'USE_CLOUDINARY': settings.USE_CLOUDINARY}
