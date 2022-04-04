import { Utils } from "./utils.js";
import { gsap } from "gsap";

export class PNIToggle {
  constructor(searchFilter) {
    this.searchFilter = searchFilter;
    this.categoryTitle = document.querySelector(`.category-title`);
    this.toggle = document.querySelector(`#product-filter-pni-toggle`);

    if (!this.toggle) {
      // TODO: this should become a throw, with enough integration tests that
      //       we can be confident that any page that should have it, has it,
      //       failing our tests on pages that should but don't.
      return console.warn(
        `Could not find the PNI filter checkbox. PNI filtering will not be available.`
      );
    }

    this.toggle.addEventListener(`change`, (evt) => {
      const doFilter = !!evt.target.checked;
      this.togglePrivacyOnly(doFilter);
    });
  }

  togglePrivacyOnly(doFilter) {
    const { searchFilter, categoryTitle } = this;

    gsap.set("figure.product-box.privacy-ding", { opacity: 1, y: 0 });
    // TODO: this might be an A/B testing opportunity to see
    //       whether users assume this toggle is a navigation
    //       action or not?
    const state = { ...history.state, filter: doFilter };
    const title = Utils.getTitle(categoryTitle.value.trim());
    history.replaceState(state, title, location.href);

    const toggleFunction = doFilter ? `add` : `remove`;
    document.body.classList[toggleFunction](`show-ding-only`);

    if (searchFilter.searchInput.value.trim()) {
      searchFilter.searchInput.focus();
      Utils.checkForEmptyNotice();
    }
  }
}
