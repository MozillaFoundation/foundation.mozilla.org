from wagtail_factories.blocks import ChooserBlockFactory


class SnippetChooserBlockFactory(ChooserBlockFactory):
    """Abstract factory for snippet chooser blocks.

    Concrete implementations should define the `model` Meta attribute and a `snippet` field
    with a subfactory pointing to the snippet factory:
        ```
        class SignupChooserBlockFactory(SnippetChooserBlockFactory):
            snippet = factory.SubFactory("foundation_cms.legacy_cms.wagtailpages.factory.Signup")

            class Meta:
                model = Signup
        ```
    """

    class Meta:
        abstract = True

    @classmethod
    def _build(cls, model_class, snippet):
        return snippet

    @classmethod
    def _create(cls, model_class, snippet):
        return snippet
