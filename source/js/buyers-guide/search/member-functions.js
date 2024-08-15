import { Utils } from "./utils.js";

const categoryTitle = document.querySelector(`.category-title`);
const parentTitle = document.querySelector(`.parent-title`);
const subcategories = document.querySelectorAll(`.subcategories`);

/**
 * ...
 * @param {*} instance
 */
export function setupNavLinks(instance) {
  const navLinks = document.querySelectorAll(
    `#multipage-nav a,.category-header,#pni-mobile-category-nav a`
  );

  for (const nav of navLinks) {
    nav.addEventListener("click", (evt) => {
      evt.stopPropagation();

      if (evt.shiftKey || evt.metaKey || evt.ctrlKey || evt.altKey) {
        return;
      }

      evt.preventDefault();

      Utils.deactivateActiveCatNav();

      document
        .querySelector("#pni-mobile-category-nav .dropdown-nav")
        .classList.remove("dropdown-nav-open");

      const { name: categoryName } = evt.target.dataset ?? {};

      if (categoryName) {
        Utils.activateCatNav(categoryName);

        instance.clearText();
        history.pushState(
          {
            title: Utils.getTitle(categoryName),
            category: categoryName,
            parent: "",
            search: "",
            filter: history.state?.filter,
            sort: history.state?.sort,
          },
          Utils.getTitle(categoryName),
          evt.target.href
        );

        document.title = Utils.getTitle(categoryName);
        instance.filterSubcategory(categoryName);
        instance.toggleSubcategory(true);
        Utils.updateHeader(categoryName, "");
        instance.filterCategory(categoryName);
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

        const { name: subcategoryName } = evt.target.dataset;

        if (subcategoryName) {
          instance.clearText();
          if (categoryTitle.value.trim() !== subcategoryName) {
            categoryTitle.value = subcategoryName;
            parentTitle.value = evt.target.dataset.parent;
            href = evt.target.href;
            instance.toggleSubcategory();
            Utils.highlightParentCategory();
          } else {
            categoryTitle.value = evt.target.dataset.parent;
            parentTitle.value = "";
            href = document.querySelector(
              `#multipage-nav a[data-name="${evt.target.dataset.parent}"],.category-header`
            ).href;
            instance.toggleSubcategory(true);
          }

          history.pushState(
            {
              title: Utils.getTitle(subcategoryName),
              category: categoryTitle.value.trim(),
              parent: parentTitle.value.trim(),
              search: "",
              filter: history.state?.filter,
              sort: history.state?.sort,
            },
            Utils.getTitle(subcategoryName),
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

/**
 * ...
 * @param {*} instance
 */
export function setupGoBackToAll(instance) {
  document
    .querySelector(`.go-back-to-all-link`)
    .addEventListener("click", (evt) => {
      evt.stopPropagation();

      if (evt.shiftKey || evt.metaKey || evt.ctrlKey || evt.altKey) {
        return;
      }

      evt.preventDefault();

      instance.clearText();
      history.pushState(
        {
          title: Utils.getTitle("None"),
          category: "None",
          parent: "",
          search: "",
          filter: history.state?.filter,
          sort: history.state?.sort,
        },
        Utils.getTitle(evt.target.dataset.name),
        evt.target.href
      );

      Utils.setActiveCatNavLink("None");

      instance.filterCategory("None");
      parentTitle.value = "";
    });
}

/**
 * ...
 * @param {*} instance
 */
export function setupReviewLinks(instance) {
  const navLinks = document.querySelectorAll(`.product-review-link`);

  if (!navLinks) return;

  for (const nav of navLinks) {
    nav.addEventListener("click", (evt) => {
      const editorialContent = document.querySelector(".editorial-content");
      const burger = document.querySelector(".burger");
      if (editorialContent) {
        evt.preventDefault();
        evt.stopPropagation();
        nav.classList.add("active");
        location.hash = "product-review";
        editorialContent.classList.add("tw-hidden");
        if (burger && burger.classList.contains("menu-open")) {
          document.querySelector(".burger").click();
        }
      }
    });
  }
}

export function toggleProductReviewView() {
  const editorialContent = document.querySelector(".editorial-content");
  const navLinks = document.querySelectorAll(`.product-review-link`);
  if (editorialContent) {
    editorialContent.classList.add("tw-hidden");
  }
  for (const nav of navLinks) {
    nav.classList.add("active");
  }
}

export function toggleCategoryRelatedArticles(category) {
  const relatedArticles = document.querySelectorAll("[data-show-for-category]");

  // Probably means we are on PNI homepage!
  if (!relatedArticles) return;
  [...relatedArticles].forEach((relatedArticle) => {
    if (category === relatedArticle.dataset.showForCategory) {
      relatedArticle.classList.remove("tw-hidden");
    } else {
      relatedArticle.classList.add("tw-hidden");
    }
  });
}
