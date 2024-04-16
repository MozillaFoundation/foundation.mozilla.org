import Accordion from "../accordion/accordion";

class NavMobileDropdown extends Accordion {
  static selector() {
    return "[data-mobile-dropdown]";
  }

  constructor(node) {
    super(node);
  }
}

export default NavMobileDropdown;
