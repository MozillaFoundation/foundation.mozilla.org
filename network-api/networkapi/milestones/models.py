from networkapi.utility.images import get_image_upload_path


def get_milestone_photo_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='milestones',
        prop_name='headline',
        instance=instance,
        current_filename=filename
    )
