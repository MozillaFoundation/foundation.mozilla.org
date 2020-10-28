const STICKY_BAR = document.getElementById(`sticky-bar`);
const ALL_PRODUCTS = document.querySelectorAll(`figure.product-box`);
const NO_RESULTS_NOTICE = document.getElementById(
  `product-filter-no-results-notice`
);
const FILTERS = [`company`, `name`, `blurb`, `worst-case`];
const SUBMIT_PRODUCT = document.querySelector(".recommend-product");

const SearchFilter = {
  init: () => {
    const searchBar = document.querySelector(`#product-filter-search`);

    if (!searchBar) {
      return console.warn(
        `Could not find the PNI search bar. Search will not be available.`
      );
    }

    const searchInput = (SearchFilter.searchInput = searchBar.querySelector(
      `input`
    ));

    searchInput.addEventListener(`input`, (evt) => {
      const searchText = searchInput.value.trim();

      if (searchText) {
        searchBar.classList.add(`has-content`);
        STICKY_BAR.classList.add(`search-active`);
      } else {
        searchBar.classList.remove(`has-content`);
      }

      SearchFilter.filter(searchText);
    });

    searchBar.addEventListener(`focus`, (_evt) => {
      // We want focus to fall through to the input element instead
      searchInput.focus();
      // And to make CSS work easier, set a class on the parent container
      // for both search and the creep-o-meter component, so that it can
      // relocate so as not to interfere with the search bar.
      STICKY_BAR.classList.add(`search-active`);
    });

    // Whenever focus is moved away from the search bar, check if we can
    // safely restore the creep-o-meter component or not.
    searchInput.addEventListener(`blur`, (_evt) => {
      if (!searchInput.value.trim()) {
        STICKY_BAR.classList.remove(`search-active`);
      }
    });

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
    };

    clear.addEventListener(`click`, (evt) => {
      evt.preventDefault();
      clearText();
    });
  },

  filter: (text) => {
    ALL_PRODUCTS.forEach((product) => {
      if (SearchFilter.test(product, text)) {
        product.classList.remove(`d-none`);
      } else {
        product.classList.add(`d-none`);
      }
    });

    SearchFilter.checkForEmptyNotice();
  },

  checkForEmptyNotice: () => {
    let qs = `figure.product-box:not(.d-none)`;

    if (document.body.classList.contains(`show-ding-only`)) {
      qs = `${qs}.privacy-ding`;
    }

    const results = document.querySelectorAll(qs);
    const count = results.length;
    const viewId = document.querySelector("body").id;
    if (count === 0) {
      NO_RESULTS_NOTICE.classList.remove(`d-none`);
      if (viewId !== "view-home") {
        SUBMIT_PRODUCT.classList.add("d-none");
      }
    } else {
      NO_RESULTS_NOTICE.classList.add(`d-none`);
      if (viewId !== "view-home") {
        SUBMIT_PRODUCT.classList.remove("d-none");
      }
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
