import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
const SORTS = [`name`, `company`, `blurb`];
const FILTERS = [`company`, `name`, `blurb`, `worst-case`];
const ALL_PRODUCTS = document.querySelectorAll(`figure.product-box`);
const SUBMIT_PRODUCT = document.querySelector(".recommend-product");
const NO_RESULTS_NOTICE = document.getElementById(
  `product-filter-no-results-notice`
);
const ALL_CATEGORY_LABEL = document.querySelector(
  `#multipage-nav .multipage-link[data-name="None"]`
).textContent;
const PARENT_TITLE = document.querySelector(`.parent-title`);

export class Utils {
  /**
   * Return the title of the page based on the category passed in the argument
   *
   * @param {String} category name of the category
   * @returns {String} title of the page
   */
  static getTitle(category) {
    if (category == "None")
      return document.querySelector('meta[name="pni-home-title"]').content;
    else {
      return `${category} | ${
        document.querySelector('meta[name="pni-category-title"]').content
      }`;
    }
  }

  /**
   * Update page header to the category passed in the argument
   *
   * @param {*} category
   * @param {*} parent
   *
   * @todo Improve the implementation to increase code readibility
   */
  static updateHeader(category, parent) {
    const headerText = document.querySelector(".category-header");

    if (parent) {
      document.querySelector(".category-header").dataset.name = parent;
      headerText.textContent = parent;
      if (document.querySelector(`#multipage-nav a[data-name="${parent}"]`)) {
        document.querySelector(".category-header").href =
          document.querySelector(
            `#multipage-nav a[data-name="${parent}"]`
          ).href;
      }
      document.querySelector(
        `#pni-mobile-category-nav .active-link-label`
      ).textContent = parent;
    } else {
      const header = category === "None" ? ALL_CATEGORY_LABEL : category;
      headerText.textContent = header;
      document.querySelector(".category-header").dataset.name = category;
      if (document.querySelector(`#multipage-nav a[data-name="${category}"]`)) {
        document.querySelector(".category-header").href =
          document.querySelector(
            `#multipage-nav a[data-name="${category}"]`
          ).href;
      }
      document.querySelector(
        `#pni-mobile-category-nav .active-link-label`
      ).textContent =
        category === "None"
          ? document.querySelector(`#multipage-nav a[data-name="None"]`)
              .textContent
          : category;
    }
  }

  /**
   * Deactivate the currently active category nav link
   */
  static deactivateActiveCatNav() {
    const linkForLarge = document.querySelector(`#multipage-nav a.active`);
    const linkForMobile = document.querySelector(
      `#pni-mobile-category-nav a.active`
    );

    // for larger screens
    if (linkForLarge) {
      linkForLarge.classList.remove(`active`);
    }

    // for small screens
    if (linkForMobile) {
      linkForMobile.classList.remove(`active`);
    }
  }

  /**
   * Activate a specific category nav link
   *
   * @param {String} category category name
   */
  static activateCatNav(category = "None") {
    const linkForLarge = document.querySelector(
      `#multipage-nav a[data-name="${category}"]`
    );
    const linkForMobile = document.querySelector(
      `#pni-mobile-category-nav a[data-name="${category}"]`
    );

    // for larger screens
    if (linkForLarge) {
      linkForLarge.classList.add(`active`);
    }

    // for small screens
    if (linkForMobile) {
      linkForMobile.classList.add(`active`);
    }
  }

  /**
   * Set active category nav link
   *
   * @param {String} category name of the category
   */
  static setActiveCatNavLink(category) {
    this.deactivateActiveCatNav();
    this.activateCatNav(category);
  }

  /**
   * Highlight parent category nav link
   */
  static highlightParentCategory() {
    this.setActiveCatNavLink(PARENT_TITLE.value.trim());
  }

  /**
   * Toggle products' visibility based on search text
   *
   * @param {String} text search text
   */
  static filterProductsBySearchText(text) {
    gsap.set(ALL_PRODUCTS, { opacity: 1, y: 0 });
    ALL_PRODUCTS.forEach((product) => {
      if (this.productContainsSearchText(product, text)) {
        product.classList.remove(`d-none`);
        product.classList.add(`d-flex`);
      } else {
        product.classList.add(`d-none`);
        product.classList.remove(`d-flex`);
      }
    });

    this.toggleCategoryAnimation();
  }

  /**
   * Scroll animation used solely for the 'All Products' section
   */
  static toggleScrollAnimation() {
    gsap.set("figure.product-box.d-flex", { opacity: 0, y: 100 });

    gsap.set("figure.product-box.d-flex:nth-child(-n+8)", {
      opacity: 1,
      y: 0,
    });

    // group products stagger animation based on mobile breakpoint
    const responsiveBatch =
      window.innerWidth > 991 ? 8 : window.innerWidth > 767 ? 6 : 4;

    ScrollTrigger.batch("figure.product-box.d-flex:nth-child(n+8)", {
      batchMax: responsiveBatch, // maximum batch size (targets)
      id: "scroll-products",
      onEnter: (batch) =>
        gsap.to(batch, {
          opacity: 1,
          y: 0,
          stagger: 0.1,
          overwrite: true,
        }),
    });
  }

  /**
   * Animation used for category selections
   */
  static toggleCategoryAnimation(initialLoad = false) {
    ScrollTrigger.getById("scroll-products")?.kill(true);
    if (document.querySelectorAll("figure.product-box.d-flex")) {
      gsap.set("figure.product-box.d-flex", { opacity: 0, y: 100 });
    }

    if (initialLoad) {
      gsap.set("figure.product-box.d-flex:nth-child(-n+8)", {
        opacity: 1,
        y: 0,
      });
    }

    gsap.to(
      initialLoad
        ? "figure.product-box.d-flex:nth-child(n+8)"
        : "figure.product-box.d-flex",
      {
        opacity: 1,
        y: 0,
        stagger: 0.1,
        overwrite: true,
      }
    );
  }

  /**
   * Toggle products' visibility based on category
   *
   * @param {String} category category name
   */
  static filterProductsByCategory(category) {
    gsap.set(ALL_PRODUCTS, { opacity: 1, y: 0 });
    ALL_PRODUCTS.forEach((product) => {
      if (this.testCategories(product, category)) {
        product.classList.remove(`d-none`);
        product.classList.add(`d-flex`);
      } else {
        product.classList.add(`d-none`);
        product.classList.remove(`d-flex`);
      }
    });
    Utils.toggleCategoryAnimation();
  }

  /**
   * Toggle CTA visibility based on category
   *
   * @param {String} category category name
   */
  static toggleCtaForCategory(category) {
    const categoryPageCta = document.getElementById("category-featured-cta");
    if (!categoryPageCta) return;
    const categoriesWithShowCtaEnabled =
      categoryPageCta.dataset.showForCategories;

    if (categoriesWithShowCtaEnabled.includes(category)) {
      categoryPageCta.classList.remove("tw-hidden");
    } else {
      categoryPageCta.classList.add("tw-hidden");
    }
  }

  /**
   * Test if any of the product fields contains the search text
   *
   * @param {Element} product DOM element of the product
   * @param {String} text search text
   * @returns {Boolean} Whether the product contains the search text
   */
  static productContainsSearchText(product, text) {
    // Note that the following is absolutely not true for all
    // languages, but it's true for the ones we use.
    text = text.toLowerCase();
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
  }

  /**
   * Check if the product belongs to the category
   *
   * @param {Element} product DOM element of the product
   * @param {String} category category name
   * @returns {Boolean} Whether the product belongs to the category
   */
  static testCategories(product, category) {
    if (category === "None") {
      return true;
    }

    // all the categories this product belongs to
    const productCategories = Array.from(
      product.querySelectorAll(".product-categories")
    );

    return productCategories.map((c) => c.value.trim()).includes(category);
  }

  /**
   * Sort the products by the default sort order
   */
  static sortFilteredProducts() {
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
  }

  /**
   * Toggle the visibility of "no results" notice
   *
   * @todo Rename to "toggleNoResultsNotice"
   */
  static checkForEmptyNotice() {
    let qs = `figure.product-box:not(.d-none)`;

    if (document.body.classList.contains(`show-ding-only`)) {
      qs = `${qs}.privacy-ding`;
    }

    const results = document.querySelectorAll(qs);

    if (results.length === 0) {
      NO_RESULTS_NOTICE.classList.remove(`d-none`);
      SUBMIT_PRODUCT.classList.add("d-none");
    } else {
      NO_RESULTS_NOTICE.classList.add(`d-none`);
      SUBMIT_PRODUCT.classList.remove("d-none");
    }
  }

  /**
   * Toggle the visibility of the creepy face and speech bubble
   */
  static toggleCreepyFace() {
    const CREEPINESS_FACE = document.querySelector(
      ".creep-o-meter-information"
    );
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

  /**
   * Sorts Products Review Cards based on history.state.sort
   * value (alphabetical, ascending/descending creepiness value)
   */
  static sortProductCards() {
    const container = document.querySelector(`.product-box-list`);
    const list = [...container.querySelectorAll(`.product-box`)];
    const getCreepinessValue = (e) => parseFloat(e.dataset.creepiness);
    const getProductTitle = (e) => e.querySelector(".product-name").innerText;
    switch (history.state?.sort) {
      case "ALPHA":
        list
          .sort((a, b) => getProductTitle(a).localeCompare(getProductTitle(b)))
          .forEach((p) => container.append(p));
        break;
      case "DESCENDING":
        list
          .sort((a, b) => getCreepinessValue(b) - getCreepinessValue(a))
          .forEach((p) => container.append(p));
        break;
      case "ASCENDING":
      default:
        list
          .sort((a, b) => getCreepinessValue(a) - getCreepinessValue(b))
          .forEach((p) => container.append(p));
        break;
    }
  }

  /**
   * Scroll to a specific subcategory nav link if it exists on the page
   *
   * @param {string} category - The name of the category
   */
  static scrollToSubCategory(category) {
    const subcatLink = document.querySelector(
      `a.subcategories[data-name="${category}"]`
    );

    if (!category || !subcatLink) return;

    subcatLink.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "start",
    });
  }
}
