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
      ALL_PRODUCTS.forEach((product) => {
        product.classList.remove(`d-none`);
        product.classList.add(`d-flex`);
      });

      history.replaceState(
        {
          ...history.state,
          search: "",
        },
        SearchFilter.getTitle(categoryTitle.value.trim()),
        location.href
      );

      SearchFilter.sortOnCreepiness();
      SearchFilter.moveCreepyFace();
    };

    clear.addEventListener(`click`, (evt) => {
      evt.preventDefault();
      SearchFilter.filterSubcategory("None");
      SearchFilter.updateHeader("None", null);
      clearText();
    });

    const navLinks = document.querySelectorAll(
      `#multipage-nav a,.category-header`
    );

    for (const nav of navLinks) {
      nav.addEventListener("click", (evt) => {
        evt.stopPropagation();

        if (evt.shiftKey || evt.metaKey || evt.ctrlKey || evt.altKey) {
          return;
        }

        evt.preventDefault();

        document
          .querySelector(`#multipage-nav a.active`)
          .classList.remove(`active`);

        if (evt.target.dataset.name) {
          document
            .querySelector(
              `#multipage-nav a[data-name="${evt.target.dataset.name}"]`
            )
            .classList.add(`active`);

          clearText();
          history.pushState(
            {
              title: SearchFilter.getTitle(evt.target.dataset.name),
              category: evt.target.dataset.name,
              parent: "",
              search: "",
              filter: history.state?.filter,
            },
            SearchFilter.getTitle(evt.target.dataset.name),
            evt.target.href
          );

          document.title = SearchFilter.getTitle(evt.target.dataset.name);
          SearchFilter.filterSubcategory(evt.target.dataset.name);
          SearchFilter.toggleSubcategory(true);
          SearchFilter.updateHeader(evt.target.dataset.name, "");
          SearchFilter.filterCategory(evt.target.dataset.name);
        }
      });
    }

    for (const subcategory of subcategories) {
      subcategory.addEventListener("click", (evt) => {
        evt.stopPropagation();

        if (evt.shiftKey || evt.metaKey || evt.ctrlKey || evt.altKey) {
          return;
        }

        evt.preventDefault();

        let href;

        if (evt.target.dataset.name) {
          clearText();
          if (categoryTitle.value.trim() !== evt.target.dataset.name) {
            categoryTitle.value = evt.target.dataset.name;
            parentTitle.value = evt.target.dataset.parent;
            href = evt.target.href;
            SearchFilter.toggleSubcategory();
            SearchFilter.highlightParent();
          } else {
            categoryTitle.value = evt.target.dataset.parent;
            parentTitle.value = "";
            href = document.querySelector(
              `#multipage-nav a[data-name="${evt.target.dataset.parent}"]`
            ).href;
            SearchFilter.toggleSubcategory(true);
          }

          history.pushState(
            {
              title: SearchFilter.getTitle(evt.target.dataset.name),
              category: categoryTitle.value.trim(),
              parent: parentTitle.value.trim(),
              search: "",
              filter: history.state?.filter,
            },
            SearchFilter.getTitle(evt.target.dataset.name),
            href
          );

          document.title = SearchFilter.getTitle(categoryTitle.value.trim());
          SearchFilter.updateHeader(
            categoryTitle.value.trim(),
            parentTitle.value.trim()
          );
          SearchFilter.filterCategory(categoryTitle.value.trim());
        }
      });
    }

    document
      .querySelector(`.go-back-to-all-link`)
      .addEventListener("click", (evt) => {
        evt.stopPropagation();

        if (evt.shiftKey || evt.metaKey || evt.ctrlKey || evt.altKey) {
          return;
        }

        evt.preventDefault();

        clearText();
        history.pushState(
          {
            title: SearchFilter.getTitle("None"),
            category: "None",
            parent: "",
            search: "",
            filter: history.state?.filter,
          },
          SearchFilter.getTitle(evt.target.dataset.name),
          evt.target.href
        );

        document
          .querySelector(`#multipage-nav a.active`)
          .classList.remove(`active`);

        document
          .querySelector(`#multipage-nav a[data-name="None"]`)
          .classList.add(`active`);

        SearchFilter.filterCategory("None");
        parentTitle.value = "";
      });

    window.addEventListener(`popstate`, (event) => {
      const { state } = event;
      if (!state) return; // if it's a "real" back, we shouldn't need to do anything

      const { title, category, parent } = state;
      document.title = title;

      if (!history.state?.search) {
        SearchFilter.clearCategories();
        categoryTitle.value = category;
        parentTitle.value = parent;

        searchBar.classList.remove(`has-content`);
        searchInput.value = ``;

        if (parent) {
          SearchFilter.highlightParent();
          SearchFilter.toggleSubcategory();
        } else {
          document
            .querySelector(`#multipage-nav a.active`)
            .classList.remove(`active`);

          document
            .querySelector(`#multipage-nav a[data-name="${category}"]`)
            .classList.add(`active`);

          SearchFilter.toggleSubcategory(true);
        }
      } else {
        SearchFilter.toggleSubcategory(true);
        searchBar.classList.add(`has-content`);
        searchInput.value = history.state?.search;
        SearchFilter.filter(history.state?.search);
      }

      SearchFilter.filterCategory(category);
      SearchFilter.filterSubcategory(category);
      SearchFilter.updateHeader(category, parent);

      if (history.state?.filter) {
        toggle.checked = history.state?.filter;

        if (history.state?.filter) {
          document.body.classList.add(`show-ding-only`);
        } else {
          document.body.classList.remove(`show-ding-only`);
        }
      }
    });

    history.replaceState(
      {
        title: SearchFilter.getTitle(categoryTitle.value.trim()),
        category: categoryTitle.value.trim(),
        parent: parentTitle.value.trim(),
        search: history.state?.search ?? "",
        filter: history.state?.filter,
      },
      SearchFilter.getTitle(categoryTitle.value.trim()),
      location.href
    );

    if (history.state?.search) {
      searchBar.classList.add(`has-content`);
      searchInput.value = history.state?.search;
      SearchFilter.filter(history.state?.search);
    } else {
      searchBar.classList.remove(`has-content`);
      searchInput.value = ``;
    }

    if (history.state?.filter) {
      toggle.checked = history.state?.filter;

      if (history.state?.filter) {
        document.body.classList.add(`show-ding-only`);
      } else {
        document.body.classList.remove(`show-ding-only`);
      }
    }
  },

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
  },

  updateHeader: (category, parent) => {
    if (parent) {
      document.querySelector(".category-header").textContent = parent;
      document.querySelector(".category-header").dataset.name = parent;
      document.querySelector(".category-header").href = document.querySelector(
        `#multipage-nav a[data-name="${parent}"]`
      ).href;
    } else {
      const header = category === "None" ? "All" : category;
      document.querySelector(".category-header").textContent = header;
      document.querySelector(".category-header").dataset.name = category;
      document.querySelector(".category-header").href = document.querySelector(
        `#multipage-nav a[data-name="${category}"]`
      ).href;
    }
  },

  filterSubcategory: (category) => {
    for (const subcategory of subcategories) {
      if (subcategory.dataset.parent === category) {
        subcategory.classList.remove(`tw-hidden`);
      } else {
        subcategory.classList.add(`tw-hidden`);
      }
    }
  },

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
      for (field of SORTS) {
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

  highlightParent: () => {
    if (document.querySelector(`#multipage-nav a.active`)) {
      document
        .querySelector(`#multipage-nav a.active`)
        .classList.remove(`active`);
    }

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

const PNIToggle = {
  init: () => {
    if (!toggle) {
      return console.warn(
        `Could not find the PNI filter checkbox. PNI filtering will not be available.`
      );
    }

    toggle.addEventListener(`change`, (evt) => {
      const filter = evt.target.checked;

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

export { SearchFilter, PNIToggle };
