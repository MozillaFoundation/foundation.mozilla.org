const ALL_PRODUCTS = document.querySelectorAll(`figure.product-box`);
const NO_RESULTS_NOTICE = document.getElementById(
  `product-filter-no-results-notice`
);
const FILTERS = [`company`, `name`, `blurb`, `worst-case`];
const SUBMIT_PRODUCT = document.querySelector(".recommend-product");
const CREEPINESS_FACE = document.querySelector(".creep-o-meter-information");

const SearchFilter = {
  init: () => {
    const searchBar = document.querySelector(`#product-filter-search`);

    if (!searchBar) {
      return console.warn(
        `Could not find the PNI search bar. Search will not be available.`
      );
    }

    const searchInput = (SearchFilter.searchInput =
      searchBar.querySelector(`input`));

    searchInput.addEventListener(`input`, (evt) => {
      const searchText = searchInput.value.trim();

      if (searchText) {
        searchBar.classList.add(`has-content`);
        SearchFilter.filter(searchText);
      }
    });

    const categoryTitle = document.querySelector(`.category-title`);

    if (categoryTitle.value.trim()) {
      SearchFilter.filterCategory(categoryTitle.value.trim());
    }

    const clear = searchBar.querySelector(`.clear-icon`);
    if (!clear) {
      return console.warn(
        `Could not find the PNI search input clear icon. Search will work, but clearing will not.`
      );
    }

    const clearText = () => {
      searchBar.classList.remove(`has-content`);
      searchInput.value = ``;
      searchInput.focus();
      ALL_PRODUCTS.forEach((product) => product.classList.remove(`d-none`));
      SearchFilter.moveCreepyFace();
    };

    clear.addEventListener(`click`, (evt) => {
      evt.preventDefault();
      clearText();
    });

    const navLinks = document.querySelectorAll(`#multipage-nav a`);

    for (const nav of navLinks) {
      nav.addEventListener("click", (evt) => {
        evt.stopPropagation();
        evt.preventDefault();

        document
          .querySelector(`#multipage-nav a.active`)
          .classList.remove(`active`);

        evt.target.classList.add(`active`);

        if (evt.target.dataset.name) {
          SearchFilter.filterCategory(evt.target.dataset.name);
        }
      });
    }

    document
      .querySelector(`.go-back-to-all-link`)
      .addEventListener("click", (evt) => {
        evt.stopPropagation();
        evt.preventDefault();

        SearchFilter.filterCategory("None");
      });
  },

  clearCategories: () => {
    SearchFilter.filterCategory("None");

    document
      .querySelector(`#multipage-nav a.active`)
      .classList.remove(`active`);
    document
      .querySelector(`#multipage-nav a[data-name="None"]`)
      .classList.add(`active`);
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
    document
      .querySelector(`#multipage-nav a.active`)
      .classList.remove(`active`);
    document
      .querySelector(`#multipage-nav a[data-name="None"]`)
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

    SearchFilter.moveCreepyFace();
    SearchFilter.checkForEmptyNotice();
  },

  filterCategory: (category) => {
    ALL_PRODUCTS.forEach((product) => {
      if (SearchFilter.testCateories(product, category)) {
        product.classList.remove(`d-none`);
        product.classList.add(`d-flex`);
      } else {
        product.classList.add(`d-none`);
        product.classList.remove(`d-flex`);
      }
    });

    SearchFilter.moveCreepyFace();
    SearchFilter.checkForEmptyNotice();
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
    let qs, data, field;

    for (field of FILTERS) {
      qs = `.product-${field}`;
      data = product.querySelector(qs);
      data = (data.value || data.textContent).toLowerCase();
      if (data.indexOf(text) !== -1) {
        return true;
      }
    }

    return false;
  },

  testCateories: (product, category) => {
    if (category === "None") {
      return true;
    }

    const productCategories = Array.from(
      product.querySelectorAll(".product-categories")
    );

    return productCategories.map((c) => c.value.trim()).includes(category);
  },
};

const PNIToggle = {
  init: () => {
    const toggle = document.querySelector(`#product-filter-pni-toggle`);

    if (!toggle) {
      return console.warn(
        `Could not find the PNI filter checkbox. PNI filtering will not be available.`
      );
    }

    toggle.addEventListener(`change`, (evt) => {
      const filter = evt.target.checked;

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

export { SearchFilter, PNIToggle };
