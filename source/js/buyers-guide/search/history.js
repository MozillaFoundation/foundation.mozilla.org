import { gsap } from "gsap";
import { Utils } from "./utils.js";
import { CreepUtils } from "./creep-utils.js";

const categoryTitle = document.querySelector(`.category-title`);
const parentTitle = document.querySelector(`.parent-title`);
const toggle = document.querySelector(`#product-filter-pni-toggle`);

/**
 * ...
 * @param {*} instance
 * @param {*} searchBar
 * @param {*} searchInput
 */
export function setupHistoryManagement(instance, searchBar, searchInput) {
  setupPopStateHandler(instance, searchBar, searchInput);
  performInitialHistoryReplace(instance, searchBar, searchInput);
}

/**
 * ...
 * @param {*} instance
 * @param {*} searchBar
 * @param {*} searchInput
 */
export function performInitialHistoryReplace(instance, searchBar, searchInput) {
  history.replaceState(
    {
      title: Utils.getTitle(categoryTitle.value.trim()),
      category: categoryTitle.value.trim(),
      parent: parentTitle.value.trim(),
      search: history.state?.search ?? "",
      filter: history.state?.filter,
    },
    Utils.getTitle(categoryTitle.value.trim()),
    location.href
  );

  if (history.state?.search) {
    searchBar.classList.add(`has-content`);
    searchInput.value = history.state?.search;
    instance.filter(history.state?.search);
  } else {
    searchBar.classList.remove(`has-content`);
    searchInput.value = ``;
  }

  if (history.state?.filter) {
    toggle.checked = history.state?.filter;

    if (history.state?.filter) {
      gsap.set("figure.product-box.privacy-ding", { opacity: 1, y: 0 });
      document.body.classList.add(`show-ding-only`);
    } else {
      document.body.classList.remove(`show-ding-only`);
    }
  }

  if (history.state?.parent && history.state?.category) {
    document
      .querySelector(`a.subcategories[data-name="${history.state?.category}"]`)
      .scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "start",
      });
  }
}

/**
 * ...
 * @param {*} instance
 * @param {*} searchBar
 * @param {*} searchInput
 */
export function setupPopStateHandler(instance, searchBar, searchInput) {
  window.addEventListener(`popstate`, (event) => {
    const { state } = event;
    if (!state) return; // if it's a "real" back, we shouldn't need to do anything

    const { title, category, parent } = state;
    document.title = title;

    if (!history.state?.search) {
      instance.clearCategories();
      categoryTitle.value = category;
      parentTitle.value = parent;

      searchBar.classList.remove(`has-content`);
      searchInput.value = ``;

      if (parent) {
        Utils.highlightParentCategory();
        instance.toggleSubcategory();
      } else {
        if (document.querySelector(`#multipage-nav a.active`)) {
          document
            .querySelector(`#multipage-nav a.active`)
            .classList.remove(`active`);
        }

        if (document.querySelector(`#pni-nav-mobile a.active`)) {
          document
            .querySelector(`#pni-nav-mobile a.active`)
            .classList.remove(`active`);
        }

        if (
          document.querySelector(`#multipage-nav a[data-name="${category}"]`)
        ) {
          document
            .querySelector(`#multipage-nav a[data-name="${category}"]`)
            .classList.add(`active`);
        }

        if (
          document.querySelector(`#pni-nav-mobile a[data-name="${category}"]`)
        ) {
          document
            .querySelector(`#pni-nav-mobile a[data-name="${category}"]`)
            .classList.add(`active`);
        }

        instance.toggleSubcategory(true);
      }
    } else {
      instance.toggleSubcategory(true);
      searchBar.classList.add(`has-content`);
      searchInput.value = history.state?.search;
      instance.filter(history.state?.search);
    }

    instance.filterCategory(category);
    instance.filterSubcategory(parent || category);
    Utils.updateHeader(category, parent);

    if (history.state?.filter) {
      toggle.checked = history.state?.filter;

      if (history.state?.filter) {
        gsap.set("figure.product-box.privacy-ding", { opacity: 1, y: 0 });
        document.body.classList.add(`show-ding-only`);
      } else {
        document.body.classList.remove(`show-ding-only`);
      }
    }
  });
}

/**
 * ...
 * @param {*} instance
 */
export function applyHistory(instance) {
  const { category, parent } = history.state;

  categoryTitle.value = category;
  parentTitle.value = parent;

  if (parent) {
    Utils.highlightParentCategory();
    instance.toggleSubcategory();
  } else {
    if (document.querySelector(`#multipage-nav a.active`)) {
      document
        .querySelector(`#multipage-nav a.active`)
        .classList.remove(`active`);
    }

    if (document.querySelector(`#pni-nav-mobile a.active`)) {
      document
        .querySelector(`#pni-nav-mobile a.active`)
        .classList.remove(`active`);
    }

    if (document.querySelector(`#multipage-nav a[data-name="${category}"]`)) {
      document
        .querySelector(`#multipage-nav a[data-name="${category}"]`)
        .classList.add(`active`);
    }

    if (document.querySelector(`#pni-nav-mobile a[data-name="${category}"]`)) {
      document
        .querySelector(`#pni-nav-mobile a[data-name="${category}"]`)
        .classList.add(`active`);
    }

    instance.toggleSubcategory(true);
  }

  instance.filterCategory(category);
  instance.filterSubcategory(parent || category);
  Utils.updateHeader(category, parent);
  CreepUtils.sortOnCreepiness();
  CreepUtils.moveCreepyFace();

  if (history.state?.parent && history.state?.category) {
    document
      .querySelector(`a.subcategories[data-name="${history.state?.category}"]`)
      .scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "start",
      });
  }
}
