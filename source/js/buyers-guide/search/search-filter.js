const ALL_PRODUCTS = document.querySelectorAll(`figure.product-box`);
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

function applyHistory(NamespaceObject) {
  const { category, parent } = history.state;

  categoryTitle.value = category;
  parentTitle.value = parent;

  if (parent) {
    NamespaceObject.highlightParent();
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
  NamespaceObject.filterCategory(category);
  NamespaceObject.filterSubcategory(parent || category);
  NamespaceObject.updateHeader(category, parent);
  NamespaceObject.sortOnCreepiness();
  NamespaceObject.moveCreepyFace();

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

function clearText(NamespaceObject, searchBar, searchInput) {
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

  NamespaceObject.sortOnCreepiness();
  NamespaceObject.moveCreepyFace();
}

/**
 * ...
 */
export class SearchFilter {
  constructor(NamespaceObject) {
    [`mousedown`, `touchstart`].forEach((type) =>
      subContainer.addEventListener(type, markScrollStart)
    );

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
        clearText(NamespaceObject, searchBar, searchInput);
        applyHistory(NamespaceObject);
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
      clearText(NamespaceObject, searchBar, searchInput);
      applyHistory(NamespaceObject);
    });

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

          clearText(NamespaceObject, searchBar, searchInput);
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
          NamespaceObject.filterSubcategory(evt.target.dataset.name);
          NamespaceObject.toggleSubcategory(true);
          NamespaceObject.updateHeader(evt.target.dataset.name, "");
          NamespaceObject.filterCategory(evt.target.dataset.name);
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
            clearText(NamespaceObject, searchBar, searchInput);
            if (categoryTitle.value.trim() !== evt.target.dataset.name) {
              categoryTitle.value = evt.target.dataset.name;
              parentTitle.value = evt.target.dataset.parent;
              href = evt.target.href;
              NamespaceObject.toggleSubcategory();
              NamespaceObject.highlightParent();
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

            document.title = NamespaceObject.getTitle(
              categoryTitle.value.trim()
            );
            NamespaceObject.updateHeader(
              categoryTitle.value.trim(),
              parentTitle.value.trim()
            );
            NamespaceObject.filterCategory(categoryTitle.value.trim());
          }
        },
        true
      );
    }

    document
      .querySelector(`.go-back-to-all-link`)
      .addEventListener("click", (evt) => {
        evt.stopPropagation();

        if (evt.shiftKey || evt.metaKey || evt.ctrlKey || evt.altKey) {
          return;
        }

        evt.preventDefault();

        clearText(NamespaceObject, searchBar, searchInput);
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

        NamespaceObject.filterCategory("None");
        parentTitle.value = "";
      });

    window.addEventListener(`popstate`, (event) => {
      const { state } = event;
      if (!state) return; // if it's a "real" back, we shouldn't need to do anything

      const { title, category, parent } = state;
      document.title = title;

      if (!history.state?.search) {
        NamespaceObject.clearCategories();
        categoryTitle.value = category;
        parentTitle.value = parent;

        searchBar.classList.remove(`has-content`);
        searchInput.value = ``;

        if (parent) {
          NamespaceObject.highlightParent();
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

      NamespaceObject.filterCategory(category);
      NamespaceObject.filterSubcategory(parent || category);
      NamespaceObject.updateHeader(category, parent);

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
        .querySelector(
          `a.subcategories[data-name="${history.state?.category}"]`
        )
        .scrollIntoView({
          behavior: "smooth",
          block: "nearest",
          inline: "start",
        });
    }
  }
}
