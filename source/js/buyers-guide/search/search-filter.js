import {
  markScrollStart,
  setupNavLinks,
  setupGoBackToAll,
  setupPopStateHandler,
  performInitialHistoryReplace,
  setupSearchBar,
} from "./member-functions.js";
import { Utils } from "./utils.js";
import { CreepUtils } from "./creep-utils.js";

const categoryTitle = document.querySelector(`.category-title`);
const parentTitle = document.querySelector(`.parent-title`);
const subcategories = document.querySelectorAll(`.subcategories`);
const subContainer = document.querySelector(`.subcategory-header`);

/**
 * ...
 */
export class SearchFilter {
  constructor() {
    [`mousedown`, `touchstart`].forEach((type) =>
      subContainer.addEventListener(type, markScrollStart)
    );
    this.setup();
  }

  setup() {
    const { searchBar, searchInput } = setupSearchBar(this);
    setupNavLinks(this, searchBar, searchInput);
    setupGoBackToAll(this, searchBar, searchInput);
    setupPopStateHandler(this, searchBar, searchInput);
    performInitialHistoryReplace(this, searchBar, searchInput);
  }

  /**
   * Searching is really "filtering", toggling visibility for products
   * based on whether they match the given text (from amongst several
   * possible product fields).
   * @param {*} text
   */
  filter(text) {
    this.clearCategories();
    this.toggleSubcategory(true);
    this.filterSubcategory("None");

    Utils.updateHeader("None", null);
    Utils.selectAllCategory();
    Utils.toggleProducts(text);

    const state = { ...history.state, search: text };
    const title = Utils.getTitle(categoryTitle.value.trim());
    history.replaceState(state, title, location.href);

    Utils.sortFilteredProducts();
    CreepUtils.moveCreepyFace();
    Utils.checkForEmptyNotice();
  }

  clearCategories() {
    this.filterCategory("None");
    parentTitle.value = null;
    Utils.clearCategories();
  }

  filterCategory(category) {
    Utils.showProductsForCategory(category);
    categoryTitle.value = category;
    CreepUtils.sortOnCreepiness();
    CreepUtils.moveCreepyFace();
    Utils.checkForEmptyNotice();
  }

  toggleSubcategory(clear = false) {
    const activeClasses = [
      "active",
      "tw-bg-gray-80",
      "tw-text-white",
      "tw-border-gray-80",
    ];

    const defaultClasses = [
      "hover:tw-border-pni-lilac",
      "hover:tw-bg-pni-lilac",
      "tw-text-gray-60",
      "tw-border-gray-20",
      "tw-bg-white",
    ];

    if (document.querySelector(`a.subcategories.active`)) {
      document
        .querySelector(`a.subcategories.active`)
        .classList.add(...defaultClasses);
      document
        .querySelector(`a.subcategories.active`)
        .classList.remove(...activeClasses);
    }

    if (clear === true) return;

    this.activateSubcategory(activeClasses, defaultClasses);
  }

  activateSubcategory(activeClasses, defaultClasses) {
    const categoryName = categoryTitle.value.trim();

    document
      .querySelector(`a.subcategories[data-name="${categoryName}"]`)
      .classList.add(...activeClasses);

    document
      .querySelector(`a.subcategories[data-name="${categoryName}"]`)
      .classList.remove(...defaultClasses);

    document
      .querySelector(`a.subcategories[data-name="${categoryName}"]`)
      .scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "start",
      });
  }

  filterSubcategory(category) {
    for (const subcategory of subcategories) {
      if (subcategory.dataset.parent === category) {
        subcategory.classList.remove(`tw-hidden`);
      } else {
        subcategory.classList.add(`tw-hidden`);
      }
    }
  }
}
