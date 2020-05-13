import FOMO_A11Y from "./a11y/fomo_assessments";
import PNI_A11Y from "./a11y/pni_assessments";
import GLOBAL_COMPONENT_A11Y from "./a11y/global_component_assessments";

describe(`Accessibility Tests`, () => {
  describe(`FoMo Page Assessments`, () => {
    //FOMO_A11Y();
  });

  describe(`PNI Page Assessments`, () => {
    PNI_A11Y();
  });

  describe(`Global Component Assessments`, () => {
    //GLOBAL_COMPONENT_A11Y();
  });
});
