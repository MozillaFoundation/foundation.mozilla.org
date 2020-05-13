from django.db.migrations.operations.models import ModelOperation


def tri_to_quad(input):
    if input is True:
        return 'Yes'
    if input is False:
        return 'No'
    return 'U'


def quad_to_tri(input):
    if input == 'Yes':
        return True
    if input == 'No':
        return False
    return None


class AlterModelBases(ModelOperation):
    """
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
