from networkapi.utility.images import get_image_upload_path


def get_people_image_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='people',
        prop_name='name',
        instance=instance,
        current_filename=filename
    )


def get_people_partnership_logo_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='people',
        prop_name='name',
        suffix='_partnership',
        instance=instance,
        current_filename=filename
    )
