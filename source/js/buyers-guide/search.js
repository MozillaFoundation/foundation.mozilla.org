import { SearchFilter as SearchFilterObject } from "./search/search-filter.js";

const ALL_PRODUCTS = document.querySelectorAll(`figure.product-box`);
const NO_RESULTS_NOTICE = document.getElementById(
  `product-filter-no-results-notice`
);
const FILTERS = [`company`, `name`, `blurb`, `worst-case`];
const SORTS = [`name`, `company`, `blurb`];
const SUBMIT_PRODUCT = document.querySelector(".recommend-product");
const CREEPINESS_FACE = document.querySelector(".creep-o-meter-information");
const categoryTitle = document.querySelector(`.category-title`);
const parentTitle = document.querySelector(`.parent-title`);
const toggle = document.querySelector(`#product-filter-pni-toggle`);
const subcategories = document.querySelectorAll(`.subcategories`);
const subContainer = document.querySelector(`.subcategory-header`);


// TODO: turn this into a static class rather than plain JS object.
const SearchFilter = {
  init: () => {
    new SearchFilterObject(SearchFilter);
  },

  // MOVED OVER
  clearCategories: () => {
    SearchFilter.filterCategory("None");
    parentTitle.value = null;

    if (document.querySelector(`#multipage-nav a.active`)) {
      document
        .querySelector(`#multipage-nav a.active`)
        .classList.remove(`active`);
      document
        .querySelector(`#multipage-nav a[data-name="None"]`)
        .classList.add(`active`);
    }

    if (document.querySelector(`#pni-nav-mobile a.active`)) {
      document
        .querySelector(`#pni-nav-mobile a.active`)
        .classList.remove(`active`);
      document
        .querySelector(`#pni-nav-mobile a[data-name="None"]`)
        .classList.add(`active`);
    }
  },
  // MOVED OVER

  // MOVED OVER
  updateHeader: (category, parent) => {
    if (parent) {
      document.querySelector(".category-header").textContent = parent;
      document.querySelector(".category-header").dataset.name = parent;
      document.querySelector(".category-header").href = document.querySelector(
        `#multipage-nav a[data-name="${parent}"]`
      ).href;
      document.querySelector(`#pni-nav-mobile .active-link-label`).textContent =
        parent;
    } else {
      const header = category === "None" ? gettext("All") : category;
      document.querySelector(".category-header").textContent = header;
      document.querySelector(".category-header").dataset.name = category;
      document.querySelector(".category-header").href = document.querySelector(
        `#multipage-nav a[data-name="${category}"]`
      ).href;
      document.querySelector(`#pni-nav-mobile .active-link-label`).textContent =
        category === "None"
          ? document.querySelector(`#multipage-nav a[data-name="None"]`)
              .textContent
          : category;
    }
  },
  // MOVED OVER

  // MOVED OVER
  filterSubcategory: (category) => {
    for (const subcategory of subcategories) {
      if (subcategory.dataset.parent === category) {
        subcategory.classList.remove(`tw-hidden`);
      } else {
        subcategory.classList.add(`tw-hidden`);
      }
    }
  },
  // MOVED OVER

  getTitle: (category) => {
    if (category == "None")
      return document.querySelector('meta[name="pni-home-title"]').content;
    else {
      return `${category} | ${
        document.querySelector('meta[name="pni-category-title"]').content
      }`;
    }
  },

  moveCreepyFace: () => {
    // When searching, check to see how many products are still visible
    // If there are no visible products, there are "no search results"
    // And when there are no search results, do not show the creepo-meter-face
    if (document.querySelectorAll(".product-box:not(.d-none)").length) {
      // If there are search results, show the creepo-meter-face
      CREEPINESS_FACE.classList.remove("d-none");
    } else {
      // If there are no search results, hide the creepo-meter-face
      CREEPINESS_FACE.classList.add("d-none");
    }
  },

  filter: (text) => {
    // remove category filters
    SearchFilter.clearCategories();
    SearchFilter.toggleSubcategory(true);
    SearchFilter.filterSubcategory("None");
    SearchFilter.updateHeader("None", null);

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

    document
      .querySelector(`#multipage-nav a[data-name="None"]`)
      .classList.add(`active`);

    document
      .querySelector(`#pni-nav-mobile a[data-name="None"]`)
      .classList.add(`active`);

    ALL_PRODUCTS.forEach((product) => {
      if (SearchFilter.test(product, text)) {
        product.classList.remove(`d-none`);
        product.classList.add(`d-flex`);
      } else {
        product.classList.add(`d-none`);
        product.classList.remove(`d-flex`);
      }
    });

    history.replaceState(
      {
        ...history.state,
        search: text,
      },
      SearchFilter.getTitle(categoryTitle.value.trim()),
      location.href
    );

    SearchFilter.sortProducts();

    SearchFilter.moveCreepyFace();
    SearchFilter.checkForEmptyNotice();
  },

  sortProducts: () => {
    const container = document.querySelector(`.product-box-list`);
    const list = [...container.querySelectorAll(`.product-box`)];

    list.sort((a, b) => {
      for (const field of SORTS) {
        const qs = `.product-${field}`;
        const [propertyA, propertyB] = [
          a.querySelector(qs),
          b.querySelector(qs),
        ];
        const [propertyNameA, propertyNameB] = [
          (propertyA.value || propertyA.textContent).toLowerCase(),
          (propertyB.value || propertyB.textContent).toLowerCase(),
        ];

        if (
          propertyNameA !== propertyNameB ||
          field === SORTS[SORTS.length - 1]
        ) {
          return propertyNameA < propertyNameB
            ? -1
            : propertyNameA > propertyNameB
            ? 1
            : 0;
        }
      }
    });

    list.forEach((p) => container.append(p));
  },

  sortOnCreepiness: () => {
    const container = document.querySelector(`.product-box-list`);
    const list = [...container.querySelectorAll(`.product-box`)];
    const creepVal = (e) => parseFloat(e.dataset.creepiness);
    list
      .sort((a, b) => creepVal(a) - creepVal(b))
      .forEach((p) => container.append(p));
  },

  // MOVED OVER
  filterCategory: (category) => {
    ALL_PRODUCTS.forEach((product) => {
      if (SearchFilter.testCategories(product, category)) {
        product.classList.remove(`d-none`);
        product.classList.add(`d-flex`);
      } else {
        product.classList.add(`d-none`);
        product.classList.remove(`d-flex`);
      }
    });

    categoryTitle.value = category;
    SearchFilter.sortOnCreepiness();
    SearchFilter.moveCreepyFace();
    SearchFilter.checkForEmptyNotice();
  },
  // MOVED OVER

  highlightParent: () => {
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

    document
      .querySelector(
        `#pni-nav-mobile a[data-name="${parentTitle.value.trim()}"]`
      )
      .classList.add(`active`);

    document
      .querySelector(
        `#multipage-nav a[data-name="${parentTitle.value.trim()}"]`
      )
      .classList.add(`active`);
  },

  toggleSubcategory: (clear = false) => {
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

    if (clear) {
      return;
    }

    document
      .querySelector(
        `a.subcategories[data-name="${categoryTitle.value.trim()}"]`
      )
      .classList.add(...activeClasses);

    document
      .querySelector(
        `a.subcategories[data-name="${categoryTitle.value.trim()}"]`
      )
      .classList.remove(...defaultClasses);

    document
      .querySelector(
        `a.subcategories[data-name="${categoryTitle.value.trim()}"]`
      )
      .scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "start",
      });
  },

  checkForEmptyNotice: () => {
    let qs = `figure.product-box:not(.d-none)`;

    if (document.body.classList.contains(`show-ding-only`)) {
      qs = `${qs}.privacy-ding`;
    }

    const results = document.querySelectorAll(qs);
    const count = results.length;
    if (count === 0) {
      NO_RESULTS_NOTICE.classList.remove(`d-none`);
      SUBMIT_PRODUCT.classList.add("d-none");
    } else {
      NO_RESULTS_NOTICE.classList.add(`d-none`);
      SUBMIT_PRODUCT.classList.remove("d-none");
    }
  },

  test: (product, text) => {
    text = text.toLowerCase(); // Note that this is absolutely not true for all languages, but it's true for us.
    let qs, data;

    for (const field of FILTERS) {
      qs = `.product-${field}`;
      data = product.querySelector(qs);
      data = (data.value || data.textContent).toLowerCase();
      if (data.indexOf(text) !== -1) {
        return true;
      }
    }

    return false;
  },

  testCategories: (product, category) => {
    if (category === "None") {
      return true;
    }

    const productCategories = Array.from(
      product.querySelectorAll(".product-categories")
    );

    return productCategories.map((c) => c.value.trim()).includes(category);
  },
};

// TODO: turn this into a static class as well
const PNIToggle = {
  init: () => {
    if (!toggle) {
      return console.warn(
        `Could not find the PNI filter checkbox. PNI filtering will not be available.`
      );
    }

    toggle.addEventListener(`change`, (evt) => {
      const filter = evt.target.checked;

      // TODO: this might be an A/B testing opportunity to see
      //       whether users assume this toggle is a navigation
      //       action or not?
      history.replaceState(
        {
          ...history.state,
          filter,
        },
        SearchFilter.getTitle(categoryTitle.value.trim()),
        location.href
      );

      if (filter) {
        document.body.classList.add(`show-ding-only`);
      } else {
        document.body.classList.remove(`show-ding-only`);
      }

      if (SearchFilter.searchInput.value.trim()) {
        SearchFilter.searchInput.focus();
        SearchFilter.checkForEmptyNotice();
      }
    });
  },
};

// bootstrap both searching and privacy-ding-filtering
SearchFilter.init();
PNIToggle.init();
