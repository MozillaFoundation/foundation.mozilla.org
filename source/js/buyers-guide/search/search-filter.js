const ALL_PRODUCTS = document.querySelectorAll(`figure.product-box`);
const CREEPINESS_FACE = document.querySelector(".creep-o-meter-information");
const NO_RESULTS_NOTICE = document.getElementById(
  `product-filter-no-results-notice`
);
const SUBMIT_PRODUCT = document.querySelector(".recommend-product");

const categoryTitle = document.querySelector(`.category-title`);
const parentTitle = document.querySelector(`.parent-title`);
const toggle = document.querySelector(`#product-filter-pni-toggle`);
const subcategories = document.querySelectorAll(`.subcategories`);
const subContainer = document.querySelector(`.subcategory-header`);

let pos = { left: 0, x: 0 };
const subClasses = subContainer.classList;

function stop(evt) {
  evt.preventDefault();
  evt.stopImmediatePropagation();
}

function markScrollStart(event) {
  stop(event);
  subClasses.add("cursor-grabbing", "select-none");

  pos = {
    left: subContainer.scrollLeft,
    x: event.clientX,
  };

  [`mousemove`, `touchmove`].forEach((type) =>
    document.addEventListener(type, markScrollMove)
  );

  [`mouseup`, `touchend`, `touchcancel`].forEach((type) =>
    document.addEventListener(type, markScrollEnd)
  );
}

function markScrollMove(event) {
  subcategories.forEach((subcategory) => {
    subcategory.classList.add("pointer-events-none");
  });
  const dx = event.clientX - pos.x;
  subContainer.scrollLeft = pos.left - dx;
}

function markScrollEnd(event) {
  stop(event);

  subcategories.forEach((subcategory) => {
    subcategory.classList.remove("pointer-events-none");
  });

  subClasses.remove("cursor-grabbing", "select-none");

  [`mousemove`, `touchmove`].forEach((type) =>
    document.removeEventListener(type, markScrollMove)
  );

  [`mouseup`, `touchend`, `touchcancel`].forEach((type) =>
    document.removeEventListener(type, markScrollEnd)
  );
}

function applyHistory(instance, NamespaceObject) {
  const { category, parent } = history.state;

  categoryTitle.value = category;
  parentTitle.value = parent;

  if (parent) {
    instance.highlightParent();
    NamespaceObject.toggleSubcategory();
  } else {
    document
      .querySelector(`#multipage-nav a.active`)
      .classList.remove(`active`);

    document
      .querySelector(`#pni-nav-mobile a.active`)
      .classList.remove(`active`);

    document
      .querySelector(`#multipage-nav a[data-name="${category}"]`)
      .classList.add(`active`);

    document
      .querySelector(`#pni-nav-mobile a[data-name="${category}"]`)
      .classList.add(`active`);

    NamespaceObject.toggleSubcategory(true);
  }
  instance.filterCategory(NamespaceObject, category);
  instance.filterSubcategory(parent || category);
  instance.updateHeader(category, parent);
  instance.sortOnCreepiness();
  instance.moveCreepyFace();

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

function clearText(instance, NamespaceObject, searchBar, searchInput) {
  searchBar.classList.remove(`has-content`);
  searchInput.value = ``;
  ALL_PRODUCTS.forEach((product) => {
    product.classList.remove(`d-none`);
    product.classList.add(`d-flex`);
  });

  history.replaceState(
    {
      ...history.state,
      search: "",
    },
    NamespaceObject.getTitle(categoryTitle.value.trim()),
    location.href
  );

  instance.sortOnCreepiness();
  instance.moveCreepyFace();
}

function setupNavLinks(instance, NamespaceObject, searchBar, searchInput) {
  const navLinks = document.querySelectorAll(
    `#multipage-nav a,.category-header,#pni-nav-mobile a`
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

      document
        .querySelector(`#pni-nav-mobile a.active`)
        .classList.remove(`active`);

      document
        .querySelector("#pni-nav-mobile .dropdown-nav")
        .classList.remove("dropdown-nav-open");

      if (evt.target.dataset.name) {
        document
          .querySelector(
            `#multipage-nav a[data-name="${evt.target.dataset.name}"]`
          )
          .classList.add(`active`);

        document
          .querySelector(
            `#pni-nav-mobile a[data-name="${evt.target.dataset.name}"]`
          )
          .classList.add(`active`);

        clearText(instance, NamespaceObject, searchBar, searchInput);
        history.pushState(
          {
            title: NamespaceObject.getTitle(evt.target.dataset.name),
            category: evt.target.dataset.name,
            parent: "",
            search: "",
            filter: history.state?.filter,
          },
          NamespaceObject.getTitle(evt.target.dataset.name),
          evt.target.href
        );

        document.title = NamespaceObject.getTitle(evt.target.dataset.name);
        instance.filterSubcategory(evt.target.dataset.name);
        NamespaceObject.toggleSubcategory(true);
        instance.updateHeader(evt.target.dataset.name, "");
        instance.filterCategory(NamespaceObject, evt.target.dataset.name);
      }
    });
  }

  for (const subcategory of subcategories) {
    subcategory.addEventListener(
      "click",
      (evt) => {
        evt.stopImmediatePropagation();
        if (evt.shiftKey || evt.metaKey || evt.ctrlKey || evt.altKey) {
          return;
        }

        evt.preventDefault();

        let href;

        if (evt.target.dataset.name) {
          clearText(instance, NamespaceObject, searchBar, searchInput);
          if (categoryTitle.value.trim() !== evt.target.dataset.name) {
            categoryTitle.value = evt.target.dataset.name;
            parentTitle.value = evt.target.dataset.parent;
            href = evt.target.href;
            NamespaceObject.toggleSubcategory();
            instance.highlightParent();
          } else {
            categoryTitle.value = evt.target.dataset.parent;
            parentTitle.value = "";
            href = document.querySelector(
              `#multipage-nav a[data-name="${evt.target.dataset.parent}"]`
            ).href;
            NamespaceObject.toggleSubcategory(true);
          }

          history.pushState(
            {
              title: NamespaceObject.getTitle(evt.target.dataset.name),
              category: categoryTitle.value.trim(),
              parent: parentTitle.value.trim(),
              search: "",
              filter: history.state?.filter,
            },
            NamespaceObject.getTitle(evt.target.dataset.name),
            href
          );

          document.title = NamespaceObject.getTitle(categoryTitle.value.trim());
          instance.updateHeader(
            categoryTitle.value.trim(),
            parentTitle.value.trim()
          );
          instance.filterCategory(NamespaceObject, categoryTitle.value.trim());
        }
      },
      true
    );
  }
}

function setupGoBackToAll(instance, NamespaceObject, searchBar, searchInput) {
  document
    .querySelector(`.go-back-to-all-link`)
    .addEventListener("click", (evt) => {
      evt.stopPropagation();

      if (evt.shiftKey || evt.metaKey || evt.ctrlKey || evt.altKey) {
        return;
      }

      evt.preventDefault();

      clearText(instance, NamespaceObject, searchBar, searchInput);
      history.pushState(
        {
          title: NamespaceObject.getTitle("None"),
          category: "None",
          parent: "",
          search: "",
          filter: history.state?.filter,
        },
        NamespaceObject.getTitle(evt.target.dataset.name),
        evt.target.href
      );

      document
        .querySelector(`#multipage-nav a.active`)
        .classList.remove(`active`);

      document
        .querySelector(`#pni-nav-mobile a.active`)
        .classList.remove(`active`);

      document
        .querySelector(`#multipage-nav a[data-name="None"]`)
        .classList.add(`active`);

      document
        .querySelector(`#pni-nav-mobile a[data-name="None"]`)
        .classList.add(`active`);

      instance.filterCategory(NamespaceObject, "None");
      parentTitle.value = "";
    });
}

function setupPopStateHandler(
  instance,
  NamespaceObject,
  searchBar,
  searchInput
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
      searchInput.value = ``;

      if (parent) {
        instance.highlightParent();
        NamespaceObject.toggleSubcategory();
      } else {
        document
          .querySelector(`#multipage-nav a.active`)
          .classList.remove(`active`);

        document
          .querySelector(`#pni-nav-mobile a.active`)
          .classList.remove(`active`);

        document
          .querySelector(`#multipage-nav a[data-name="${category}"]`)
          .classList.add(`active`);

        document
          .querySelector(`#pni-nav-mobile a[data-name="${category}"]`)
          .classList.add(`active`);

        NamespaceObject.toggleSubcategory(true);
      }
    } else {
      NamespaceObject.toggleSubcategory(true);
      searchBar.classList.add(`has-content`);
      searchInput.value = history.state?.search;
      NamespaceObject.filter(history.state?.search);
    }

    instance.filterCategory(NamespaceObject, category);
    instance.filterSubcategory(parent || category);
    instance.updateHeader(category, parent);

    if (history.state?.filter) {
      toggle.checked = history.state?.filter;

      if (history.state?.filter) {
        document.body.classList.add(`show-ding-only`);
      } else {
        document.body.classList.remove(`show-ding-only`);
      }
    }
  });
}

function performInitialHistoryReplace(
  instance,
  NamespaceObject,
  searchBar,
  searchInput
) {
  history.replaceState(
    {
      title: NamespaceObject.getTitle(categoryTitle.value.trim()),
      category: categoryTitle.value.trim(),
      parent: parentTitle.value.trim(),
      search: history.state?.search ?? "",
      filter: history.state?.filter,
    },
    NamespaceObject.getTitle(categoryTitle.value.trim()),
    location.href
  );

  if (history.state?.search) {
    searchBar.classList.add(`has-content`);
    searchInput.value = history.state?.search;
    NamespaceObject.filter(history.state?.search);
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

function setupSearchBar(instance, NamespaceObject) {
  const searchBar = document.querySelector(`#product-filter-search`);

  if (!searchBar) {
    return console.warn(
      `Could not find the PNI search bar. Search will not be available.`
    );
  }

  const searchInput = (NamespaceObject.searchInput =
    searchBar.querySelector(`input`));

  searchInput.addEventListener(`input`, (evt) => {
    const searchText = searchInput.value.trim();

    if (searchText) {
      searchBar.classList.add(`has-content`);
      NamespaceObject.filter(searchText);
    } else {
      clearText(instance, NamespaceObject, searchBar, searchInput);
      applyHistory(instance, NamespaceObject);
    }
  });

  const clear = searchBar.querySelector(`.clear-icon`);
  if (!clear) {
    return console.warn(
      `Could not find the PNI search input clear icon. Search will work, but clearing will not.`
    );
  }

  clear.addEventListener(`click`, (evt) => {
    evt.preventDefault();
    searchInput.focus();
    clearText(instance, NamespaceObject, searchBar, searchInput);
    applyHistory(instance, NamespaceObject);
  });

  return { searchBar, searchInput };
}

/**
 * ...
 */
export class SearchFilter {
  constructor(NamespaceObject) {
    [`mousedown`, `touchstart`].forEach((type) =>
      subContainer.addEventListener(type, markScrollStart)
    );

    const { searchBar, searchInput } = setupSearchBar(this, NamespaceObject);
    setupNavLinks(this, NamespaceObject, searchBar, searchInput);
    setupGoBackToAll(this, NamespaceObject, searchBar, searchInput);
    setupPopStateHandler(this, NamespaceObject, searchBar, searchInput);
    performInitialHistoryReplace(this, NamespaceObject, searchBar, searchInput);
  }

  // Candidate for moving into utils
  clearCategories() {
    this.filterCategory("None");
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
  }

  filterCategory(NamespaceObject, category) {
    ALL_PRODUCTS.forEach((product) => {
      if (this.testCategories(product, category)) {
        product.classList.remove(`d-none`);
        product.classList.add(`d-flex`);
      } else {
        product.classList.add(`d-none`);
        product.classList.remove(`d-flex`);
      }
    });

    categoryTitle.value = category;
    this.sortOnCreepiness();
    this.moveCreepyFace();
    this.checkForEmptyNotice();
  }

  // Candidate for moving into utils
  testCategories(product, category) {
    if (category === "None") {
      return true;
    }

    const productCategories = Array.from(
      product.querySelectorAll(".product-categories")
    );

    return productCategories.map((c) => c.value.trim()).includes(category);
  }

  // Candidate for moving into utils
  filterSubcategory(category) {
    for (const subcategory of subcategories) {
      if (subcategory.dataset.parent === category) {
        subcategory.classList.remove(`tw-hidden`);
      } else {
        subcategory.classList.add(`tw-hidden`);
      }
    }
  }

  // Candidate for moving into utils
  updateHeader(category, parent) {
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
  }

  // Candidate for moving into utils
  highlightParent() {
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
  }

  // Candidate for moving into utils
  sortOnCreepiness() {
    const container = document.querySelector(`.product-box-list`);
    const list = [...container.querySelectorAll(`.product-box`)];
    const creepVal = (e) => parseFloat(e.dataset.creepiness);
    list
      .sort((a, b) => creepVal(a) - creepVal(b))
      .forEach((p) => container.append(p));
  }

  // Candidate for moving into utils
  moveCreepyFace() {
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
  }

  //  Candidate for moving into utils
  checkForEmptyNotice() {
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
  }
}
