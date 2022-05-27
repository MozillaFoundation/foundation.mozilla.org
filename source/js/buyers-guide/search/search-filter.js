import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Utils } from "./utils.js";
import { CreepUtils } from "./creep-utils.js";
import { markScrollStart } from "./slider-area.js";
import { setupHistoryManagement, applyHistory } from "./history.js";
import { setupNavLinks, setupGoBackToAll } from "./member-functions.js";
/**
 * ...
 */
export class SearchFilter {
  constructor() {
    gsap.registerPlugin(ScrollTrigger);
    gsap.defaults({ ease: "power3" });
    gsap.config({
      nullTargetWarn: false,
    });
    this.allProducts = document.querySelectorAll(`figure.product-box`);
    this.categoryTitle = document.querySelector(`.category-title`);

    const { searchBar, searchInput } = this.setupSearchBar();
    setupNavLinks(this);
    setupGoBackToAll(this);
    setupHistoryManagement(this, searchBar, searchInput);

    const subContainer = document.querySelector(`.subcategory-header`);
    [`mousedown`, `touchstart`].forEach((type) =>
      subContainer.addEventListener(type, markScrollStart)
    );

    // we want the animation to start when the first eight products images are loaded
    Promise.allSettled(
      Array.from(
        document.querySelectorAll(".product-box.d-flex img.product-thumbnail")
      )
        .slice(0, 8)
        .filter((img) => !img.complete)
        .map(
          (img) =>
            new Promise((resolve, reject) => {
              img.onload = resolve;
              img.onerror = reject;
            })
        )
    ).then(() => {
      if (this.categoryTitle.value === "None") {
        Utils.toggleScrollAnimation(true);
      } else {
        Utils.toggleCategoryAnimation(true);
      }
    });
  }

  /**
   * Set up the search filter functionality, and return the
   * searchbar and searchinput elements for external function
   * binding purposes.
   */
  setupSearchBar() {
    const searchBar = (this.searchBar = document.querySelector(
      `#product-filter-search`
    ));

    if (!searchBar) {
      return console.warn(
        `Could not find the PNI search bar. Search will not be available.`
      );
    }

    const debounce = (fn, ms = 0) => {
      let timeoutId;
      return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), ms);
      };
    };

    const searchInput = (this.searchInput = searchBar.querySelector(`input`));

    searchInput.addEventListener(
      `input`,
      debounce(() => {
        const searchText = searchInput.value.trim();

        if (searchText) {
          searchBar.classList.add(`has-content`);
          this.filter(searchText);
        } else {
          this.clearText();
          applyHistory(this);
        }
      }, 500)
    );

    const clear = searchBar.querySelector(`.clear-icon`);
    if (!clear) {
      return console.warn(
        `Could not find the PNI search input clear icon. Search will work, but clearing will not.`
      );
    }

    clear.addEventListener(`click`, (evt) => {
      evt.preventDefault();
      searchInput.focus();
      this.clearText();
      applyHistory(this);
    });

    return { searchBar, searchInput };
  }

  /**
   * Clear the search text
   */
  clearText() {
    const { searchBar, searchInput } = this;
    searchBar.classList.remove(`has-content`);
    searchInput.value = ``;

    gsap.set(this.allProducts, { opacity: 1, scale: 1 });
    this.allProducts.forEach((product) => {
      product.classList.remove(`d-none`);
      product.classList.add(`d-flex`);
    });

    CreepUtils.sortOnCreepiness();
    CreepUtils.moveCreepyFace();

    const state = { ...history.state, search: "" };
    const title = Utils.getTitle(this.categoryTitle.value.trim());
    history.replaceState(state, title, location.href);
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
    const title = Utils.getTitle(this.categoryTitle.value.trim());
    history.replaceState(state, title, location.href);

    Utils.sortFilteredProducts();
    CreepUtils.moveCreepyFace();
    Utils.checkForEmptyNotice();
  }

  clearCategories() {
    const parentTitle = document.querySelector(`.parent-title`);
    parentTitle.value = null;
    this.filterCategory("None");
    Utils.clearCategories();
  }

  filterCategory(category) {
    Utils.showProductsForCategory(category);
    this.categoryTitle.value = category;
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
      "hover:tw-border-blue-10",
      "hover:tw-bg-blue-10",
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
    const categoryName = this.categoryTitle.value.trim();

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
    const subcategories = document.querySelectorAll(`.subcategories`);
    for (const subcategory of subcategories) {
      if (subcategory.dataset.parent === category) {
        subcategory.classList.remove(`tw-hidden`);
      } else {
        subcategory.classList.add(`tw-hidden`);
      }
    }
  }
}
