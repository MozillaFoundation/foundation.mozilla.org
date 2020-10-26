const ALL_PRODUCTS = document.querySelectorAll(`figure.product-box`);

const FILTERS = [`company`, `name`, `blurb`, `worst-case`];

const SearchFilter = {
  init: () => {
    const searchBar = document.querySelector(`#product-filter-search`);

    if (!searchBar) {
      return console.warn(
        `Could not find the PNI search bar. Search will not be available.`
      );
    }

    const searchInput = searchBar.querySelector(`input`);

    searchInput.addEventListener(`input`, (evt) => {
      const searchText = evt.target.value.trim();

      if (searchText) {
        searchBar.classList.add(`has-content`);
      }

      SearchFilter.filter(searchText);
    });

    // we want focus to fall through to the input element instead
    searchBar.addEventListener(`focus`, (evt) => searchInput.focus());

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
    });
  },
};

export { SearchFilter, PNIToggle };
