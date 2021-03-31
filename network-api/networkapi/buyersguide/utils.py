from django.db.migrations.operations.models import ModelOperation
from networkapi.utility.images import get_image_upload_path


def get_category_og_image_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='buyersguide',
        prop_name='name',
        instance=instance,
        current_filename=filename
    )


class AlterModelBases(ModelOperation):
    """
    # TODO: This isn't being used anywhere else. Determine if we still need this class.
    See https://stackoverflow.com/a/61723620/740553
    """

    reduce_to_sql = False
    reversible = True

    def __init__(self, name, bases):
        self.bases = bases
        super().__init__(name)

    def state_forwards(self, app_label, state):
        state.models[app_label, self.name_lower].bases = self.bases
        state.reload_model(app_label, self.name_lower)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def describe(self):
        return "Update %s bases to %s" % (self.name, self.bases)
