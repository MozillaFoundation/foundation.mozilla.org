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
   *...
   * @param {*} category
   * @returns
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
   * ...
   * @param {*} category
   * @param {*} parent
   */
  static updateHeader(category, parent) {
    const headerText = document.querySelector(".category-header");

    if (parent) {
      headerText.textContent = parent;
      document.querySelector(".category-header").dataset.name = parent;
      document.querySelector(".category-header").href = document.querySelector(
        `#multipage-nav a[data-name="${parent}"]`
      ).href;
      document.querySelector(`#pni-nav-mobile .active-link-label`).textContent =
        parent;
    } else {
      const header = category === "None" ? ALL_CATEGORY_LABEL : category;
      headerText.textContent = header;
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

  /**
   * ...
   */
  static clearCategories() {
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

  /**
   * ...
   */
  static selectAllCategory() {
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
  }

  /**
   *
   */
  static highlightParentCategory() {
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
        `#pni-nav-mobile a[data-name="${PARENT_TITLE.value.trim()}"]`
      )
      .classList.add(`active`);

    document
      .querySelector(
        `#multipage-nav a[data-name="${PARENT_TITLE.value.trim()}"]`
      )
      .classList.add(`active`);
  }

  /**
   * ...
   * @param {*} text
   */
  static toggleProducts(text) {
    gsap.set(ALL_PRODUCTS, { opacity: 1, y: 0 });
    ALL_PRODUCTS.forEach((product) => {
      if (this.test(product, text)) {
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
   * Scroll Animation used solely for the 'All Products' section
   */
  static toggleScrollAnimation() {
    ScrollTrigger.clearScrollMemory();
    ScrollTrigger.refresh(true);
    gsap.set("figure.product-box.d-flex", { opacity: 0, y: 100 });

    // group products stagger animation based on mobile breakpoint
    const responsiveBatch =
      window.innerWidth > 991 ? 8 : window.innerWidth > 767 ? 6 : 4;

    ScrollTrigger.batch("figure.product-box.d-flex", {
      batchMax: responsiveBatch, // maximum batch size (targets)
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
  static toggleCategoryAnimation() {
    gsap.set("figure.product-box.d-flex", { opacity: 0, y: 100 });

    gsap.to("figure.product-box.d-flex", {
      opacity: 1,
      y: 0,
      stagger: 0.1,
      overwrite: true,
    });
  }

  /**
   * ...
   * @param {*} category
   */
  static showProductsForCategory(category) {
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

    if (category === "None") {
      Utils.toggleScrollAnimation();
    } else {
      Utils.toggleCategoryAnimation();
    }
  }

  /**
   * ...
   * @param {*} product
   * @param {*} text
   * @returns
   */
  static test(product, text) {
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
   * ...
   * @param {*} product
   * @param {*} category
   * @returns
   */
  static testCategories(product, category) {
    if (category === "None") {
      return true;
    }

    const productCategories = Array.from(
      product.querySelectorAll(".product-categories")
    );

    return productCategories.map((c) => c.value.trim()).includes(category);
  }

  /**
   * ...
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
   *
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
}
