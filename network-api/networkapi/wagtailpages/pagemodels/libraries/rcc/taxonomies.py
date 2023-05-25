from wagtail.snippets import models as snippet_models

from networkapi.wagtailpages.pagemodels.taxonomy import BaseTaxonomy


@snippet_models.register_snippet
class RCCContentType(BaseTaxonomy):
    pass


@snippet_models.register_snippet
class RCCCurricularArea(BaseTaxonomy):
    pass


@snippet_models.register_snippet
class RCCTopic(BaseTaxonomy):
    pass
