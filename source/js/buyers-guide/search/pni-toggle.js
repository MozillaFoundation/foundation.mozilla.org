import { Utils } from "./utils.js";
import { gsap } from "gsap";

export class PNIToggle {
  constructor(searchFilter) {
    this.searchFilter = searchFilter;
    this.categoryTitle = document.querySelector(`.category-title`);
    this.toggle = document.querySelector(`#product-filter-pni-toggle`);
    this.toggleContainer = document.querySelector("#product-filter-pni");

    if (!this.toggle) {
      // TODO: this should become a throw, with enough integration tests that
      //       we can be confident that any page that should have it, has it,
      //       failing our tests on pages that should but don't.
      return console.warn(
        `Could not find the PNI filter checkbox. PNI filtering will not be available.`
      );
    }

    const activeClasses = [
      "active",
      "tw-bg-gray-80",
      "tw-text-white",
      "tw-border-gray-80",
    ];

    const defaultClasses = [
      "hover:tw-border-blue-10",
      "hover:tw-bg-blue-10",
      "tw-text-gray-60",
      "tw-border-gray-20",
      "tw-bg-white",
    ];

    if (this.toggle.checked) {
      this.toggleContainer.classList.remove(...defaultClasses);
      this.toggleContainer.classList.add(...activeClasses);
    }

    this.toggle.addEventListener(`change`, (evt) => {
      const doFilter = !!evt.target.checked;

      if (!doFilter) {
        this.toggleContainer.classList.add(...defaultClasses);
        this.toggleContainer.classList.remove(...activeClasses);
      } else {
        this.toggleContainer.classList.remove(...defaultClasses);
        this.toggleContainer.classList.add(...activeClasses);
      }
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
