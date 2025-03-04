import { gsap } from "gsap";
import { Utils } from "./utils.js";

const categoryTitle = document.querySelector(`.category-title`);
const parentTitle = document.querySelector(`.parent-title`);
const toggle = document.querySelector(`#product-filter-pni-toggle`);

/**
 * Set up history management
 *
 * @param {*} instance
 * @param {Element} searchBar - The search bar element
 * @param {Element} searchInput - The search input element
 * @param {Element} mobileSearchBar - The mobile search bar element
 * @param {Element} mobileSearchInput - The mobile search input element
 */
export function setupHistoryManagement(
  instance,
  searchBar,
  searchInput,
  mobileSearchBar,
  mobileSearchInput
) {
  setupPopStateHandler(
    instance,
    searchBar,
    searchInput,
    mobileSearchBar,
    mobileSearchInput
  );
  performInitialHistoryReplace(
    instance,
    searchBar,
    searchInput,
    mobileSearchBar,
    mobileSearchInput
  );
}

/**
 * Update History state and update page UI accordingly
 *
 * @param {*} instance
 * @param {Element} searchBar - The search bar element
 * @param {Element} searchInput - The search input element
 * @param {Element} mobileSearchBar - The mobile search bar element
 * @param {Element} mobileSearchInput - The mobile search input element
 *
 * @todo FIXME. We need to revisit and improve the implementation of this function.
 *       It's unclear why history.replaceState needs to be called twice.
 *       It's also unclear why there are repeated if-else statements especially for search parameters.
 *       Further investigation is needed to understand the purpose of this function.
 */
export function performInitialHistoryReplace(
  instance,
  searchBar,
  searchInput,
  mobileSearchBar,
  mobileSearchInput
) {
  history.replaceState(
    {
      title: Utils.getTitle(categoryTitle.value.trim()),
      category: categoryTitle.value.trim(),
      parent: parentTitle.value.trim(),
      search: history.state?.search ?? "",
      filter: history.state?.filter,
      sort: history.state?.sort ?? "ASCENDING",
    },
    Utils.getTitle(categoryTitle.value.trim()),
    location.href
  );

  if (history.state?.search) {
    searchBar.classList.add(`has-content`);
    searchInput.value = history.state?.search;
    mobileSearchBar.classList.add(`has-content`);
    mobileSearchInput.value = history.state?.search;
    instance.filter(history.state?.search);
  } else {
    searchBar.classList.remove(`has-content`);
    searchInput.value = ``;
    mobileSearchBar.classList.remove(`has-content`);
    mobileSearchInput.value = ``;
  }

  const url = new URLSearchParams(window.location.search);
  const searchParameter = url.get("search");
  if (searchParameter) {
    history.replaceState(
      {
        title: Utils.getTitle(categoryTitle.value.trim()),
        category: categoryTitle.value.trim(),
        parent: parentTitle.value.trim(),
        search: searchParameter ?? "",
        filter: history.state?.filter,
        sort: history.state?.sort,
      },
      Utils.getTitle(categoryTitle.value.trim()),
      location.href
    );

    searchBar.classList.add(`has-content`);
    searchInput.value = history.state?.search;
    mobileSearchBar.classList.add(`has-content`);
    mobileSearchInput.value = history.state?.search;
    instance.filter(history.state?.search);
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
    Utils.scrollToSubCategory(history.state?.category);
  }

  // sorting priorities change when search text is applied
  if (searchParameter) {
    Utils.sortFilteredProducts();
  } else {
    Utils.sortProductCards();
  }
}

/**
 *  Set up the window.popstate event listener
 *
 * @param {*} instance
 * @param {Element} searchBar - The search bar element
 * @param {Element} searchInput - The search input element
 * @param {Element} mobileSearchBar - The mobile search bar element
 * @param {Element} mobileSearchInput - The mobile search input element
 */
export function setupPopStateHandler(
  instance,
  searchBar,
  searchInput,
  mobileSearchBar,
  mobileSearchInput
) {
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
      mobileSearchBar.classList.remove(`has-content`);
      searchInput.value = ``;
      mobileSearchInput.value = ``;

      if (parent) {
        Utils.highlightParentCategory();
        instance.toggleSubcategory();
      } else {
        Utils.setActiveCatNavLink(category);
        instance.toggleSubcategory(true);
      }
    } else {
      instance.toggleSubcategory(true);
      searchBar.classList.add(`has-content`);
      searchInput.value = history.state?.search;
      mobileSearchBar.classList.add(`has-content`);
      mobileSearchInput.value = history.state?.search;
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
 * Apply data stored in the history state to the page
 *
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
    Utils.setActiveCatNavLink(category);
    instance.toggleSubcategory(true);
  }

  instance.filterCategory(category);
  instance.filterSubcategory(parent || category);
  Utils.updateHeader(category, parent);
  Utils.sortProductCards();
  Utils.toggleCreepyFace();

  if (history.state?.parent && history.state?.category) {
    Utils.scrollToSubCategory(history.state?.category);
  }
}
