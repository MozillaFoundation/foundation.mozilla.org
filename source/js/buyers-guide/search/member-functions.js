import { Utils } from "./utils.js";
import { CreepUtils } from "./creep-utils.js";

let pos = { left: 0, x: 0 };

const ALL_PRODUCTS = document.querySelectorAll(`figure.product-box`);
const categoryTitle = document.querySelector(`.category-title`);
const parentTitle = document.querySelector(`.parent-title`);
const subcategories = document.querySelectorAll(`.subcategories`);
const subContainer = document.querySelector(`.subcategory-header`);
const subClasses = subContainer.classList;
const toggle = document.querySelector(`#product-filter-pni-toggle`);

function stop(evt) {
  evt.preventDefault();
  evt.stopImmediatePropagation();
}

export function markScrollStart(event) {
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

export function markScrollMove(event) {
  subcategories.forEach((subcategory) => {
    subcategory.classList.add("pointer-events-none");
  });
  const dx = event.clientX - pos.x;
  subContainer.scrollLeft = pos.left - dx;
}

export function markScrollEnd(event) {
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

export function applyHistory(instance) {
  const { category, parent } = history.state;

  categoryTitle.value = category;
  parentTitle.value = parent;

  if (parent) {
    instance.highlightParent();
    instance.toggleSubcategory();
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

export function clearText(instance, searchBar, searchInput) {
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
    Utils.getTitle(categoryTitle.value.trim()),
    location.href
  );

  CreepUtils.sortOnCreepiness();
  CreepUtils.moveCreepyFace();
}

export function setupNavLinks(instance, searchBar, searchInput) {
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

        clearText(instance, searchBar, searchInput);
        history.pushState(
          {
            title: Utils.getTitle(evt.target.dataset.name),
            category: evt.target.dataset.name,
            parent: "",
            search: "",
            filter: history.state?.filter,
          },
          Utils.getTitle(evt.target.dataset.name),
          evt.target.href
        );

        document.title = Utils.getTitle(evt.target.dataset.name);
        instance.filterSubcategory(evt.target.dataset.name);
        instance.toggleSubcategory(true);
        Utils.updateHeader(evt.target.dataset.name, "");
        instance.filterCategory(evt.target.dataset.name);
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
          clearText(instance, searchBar, searchInput);
          if (categoryTitle.value.trim() !== evt.target.dataset.name) {
            categoryTitle.value = evt.target.dataset.name;
            parentTitle.value = evt.target.dataset.parent;
            href = evt.target.href;
            instance.toggleSubcategory();
            instance.highlightParent();
          } else {
            categoryTitle.value = evt.target.dataset.parent;
            parentTitle.value = "";
            href = document.querySelector(
              `#multipage-nav a[data-name="${evt.target.dataset.parent}"]`
            ).href;
            instance.toggleSubcategory(true);
          }

          history.pushState(
            {
              title: Utils.getTitle(evt.target.dataset.name),
              category: categoryTitle.value.trim(),
              parent: parentTitle.value.trim(),
              search: "",
              filter: history.state?.filter,
            },
            Utils.getTitle(evt.target.dataset.name),
            href
          );

          document.title = Utils.getTitle(categoryTitle.value.trim());
          Utils.updateHeader(
            categoryTitle.value.trim(),
            parentTitle.value.trim()
          );
          instance.filterCategory(categoryTitle.value.trim());
        }
      },
      true
    );
  }
}

export function setupGoBackToAll(instance, searchBar, searchInput) {
  document
    .querySelector(`.go-back-to-all-link`)
    .addEventListener("click", (evt) => {
      evt.stopPropagation();

      if (evt.shiftKey || evt.metaKey || evt.ctrlKey || evt.altKey) {
        return;
      }

      evt.preventDefault();

      clearText(instance, searchBar, searchInput);
      history.pushState(
        {
          title: Utils.getTitle("None"),
          category: "None",
          parent: "",
          search: "",
          filter: history.state?.filter,
        },
        Utils.getTitle(evt.target.dataset.name),
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

      instance.filterCategory("None");
      parentTitle.value = "";
    });
}

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
        instance.highlightParent();
        instance.toggleSubcategory();
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
        document.body.classList.add(`show-ding-only`);
      } else {
        document.body.classList.remove(`show-ding-only`);
      }
    }
  });
}

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

export function setupSearchBar(instance) {
  const searchBar = document.querySelector(`#product-filter-search`);

  if (!searchBar) {
    return console.warn(
      `Could not find the PNI search bar. Search will not be available.`
    );
  }

  const searchInput = (instance.searchInput = searchBar.querySelector(`input`));

  searchInput.addEventListener(`input`, (evt) => {
    const searchText = searchInput.value.trim();

    if (searchText) {
      searchBar.classList.add(`has-content`);
      instance.filter(searchText);
    } else {
      clearText(instance, searchBar, searchInput);
      applyHistory(instance);
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
    clearText(instance, searchBar, searchInput);
    applyHistory(instance);
  });

  return { searchBar, searchInput };
}
