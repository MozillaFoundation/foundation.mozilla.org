import { GoogleAnalytics } from "../common";

/**
 * Based on given page title and product name, generate an object to use for GA events
 * @param {String} pageTitle page title
 * @param {String} productName product name
 * @returns {Object} Object that contains info to send to GA
 */
function getQuerySelectorEvents(pageTitle, productName) {
  return {
    // "site-wide" events
    "[data-donate-header-button]": {
      event: `donate_header_button`,
      category: `buyersguide`,
      action: `donate tap`,
      label: `${pageTitle} donate header`,
    },

    // product events
    "#product-company-url": {
      event: `product_company_link_tap`,
      category: `product`,
      action: `company link tap`,
      label: `company link for ${productName}`,
      transport: `beacon`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
    },
    "#product-live-chat": {
      event: `customer_support_link_tap`,
      category: `product`,
      action: `customer support link tap`,
      label: `support link for ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
      // Not all products have live-chat
      optional_element: true,
    },
    "#product-email": {
      event: `email_link_tap`,
      category: `product`,
      action: `email link tap`,
      label: `email link for ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
      // Not all products have email
      optional_element: true,
    },
    "#product-twitter": {
      event: `twitter_link_tap`,
      category: `product`,
      action: `twitter link tap`,
      label: `twitter link for ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
      // Not all products have Twitter
      optional_element: true,
    },
    "#creep-vote-btn": {
      event: `opinion_submitted`,
      category: `product`,
      action: `opinion submitted`,
      label: `opinion on ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
    },
    "a.privacy-policy-link": {
      event: `privacy_policy_link_tap`,
      category: `product`,
      action: `privacy policy link tap`,
      label: `policy link for ${productName}`,
      transport: `beacon`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
    },
    ".product-update-link": {
      event: `update_article_link_tap`,
      category: `product`,
      action: `update article link tap`,
      label: `update article link for ${productName}`,
      transport: `beacon`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
      // Note all products have updates
      optional_element: true,
    },
    "#mss-link": {
      event: `minimum_security_standards_link_tap`,
      category: `product`,
      action: `minimum security standards link tap`,
      label: `mss link for ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
    },
    ".btn-recommend": {
      event: `submit_a_product_button_tap`,
      category: `buyersguide`,
      action: `submit a product button tap`,
      label: `submit a product button tap on ${pageTitle}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `.btn-recommend`,
    },
  };
}

/**
 * Binds ReactGA.event to element's click event handler
 * @param {HTMLElement} element
 * @param {Object} eventData data to send as GA event
 */
function setupElementGA(element, eventData) {
  element.addEventListener(
    "click",
    () => window.dataLayer.push(eventData),
    true
  );
}

/**
 * Binds ReactGA.event to checkbox's click event handler
 * Tracks only when users tick off the checkbox (and not when they uncheck it)
 * @param {*} selector query selector
 * @param {*} eventData data to send as GA event
 */
function bindCheckboxCheckedGA(selector, eventData) {
  const checkbox = document.querySelector(selector);

  if (!checkbox) {
    console.error(`cannot find ${selector}`);
    return;
  }

  checkbox.addEventListener(
    "change",
    () => {
      if (checkbox.checked) {
        window.dataLayer.push(eventData);
      }
    },
    true
  );
}

/**
 * Binds ReactGA.event to search box's keydown event handler
 * GA Event gets sent when user triggers the keydown event for the first time during the current page session
 */
function trackSearchBoxUsage() {
  const SESSION_KEY = `searchBoxUsed`;
  const selector = `body.catalog #product-filter-search-input`;
  const searchBox = document.querySelector(selector);

  if (!searchBox) {
    console.error(`cannot find ${selector}`);
    return;
  }

  searchBox.addEventListener(
    "keydown",
    () => {
      let searchBoxUsed = sessionStorage.getItem(SESSION_KEY);

      if (!searchBoxUsed) {
        window.dataLayer.push({
          event: `type_in_search_box`,
          category: `buyersguide`,
          action: `type in search box`,
          label: `search box used`,
        });
      }

      sessionStorage.setItem(SESSION_KEY, true);
    },
    true
  );
}

/**
 * Binds ReactGA.event to "Go Back to All Products" link's click event handler
 */
function trackGoBackToAllProductsLink() {
  const link = document.querySelector("body.catalog .go-back-to-all-link");
  const searchBox = document.querySelector(
    "body.catalog input#product-filter-search-input"
  );

  if (!(link && searchBox)) {
    console.error(`cannot find DOM nodes`);
    return;
  }

  link.addEventListener(
    "click",
    () => {
      window.dataLayer.push({
        event: `product_not_found_all_link_tap`,
        category: `buyersguide`,
        action: `product not found All link tap`,
        label: `All link tap for ${searchBox.value}`,
      });
    },
    true
  );
}

/**
 * GA event setter
 */
const ProductGA = {
  /**
   * Binds ReactGA.event to various elements' event handlers
   */
  init: () => {
    if (GoogleAnalytics.doNotTrack) {
      // explicit check on DNT left in, to prevent
      // a whole heap of code from executing.
      return;
    }

    let productBox = document.querySelector(`.product-detail .tw-h1-heading`);
    let productName = productBox ? productBox.textContent : `unknown product`;
    let pageTitle = document.title;
    let querySelectorEvents = getQuerySelectorEvents(pageTitle, productName);

    Object.keys(querySelectorEvents).forEach((querySelector) => {
      let target = document;

      // Some events should only get bound on specific page(s),
      // so we need to test to see what our query target is:
      const baseData = querySelectorEvents[querySelector];
      const conditionalQuery = baseData.conditionalQuery;

      if (conditionalQuery) {
        // Are we on the right page for this event binding?
        target = document.querySelector(conditionalQuery);
        if (!target) {
          // We are not.
          return;
        }
      }

      // If we get here, we're on the right page for this event binding.
      let elements = target.querySelectorAll(querySelector);

      if (elements.length > 0) {
        const eventData = {
          event: baseData.event,
          category: baseData.category,
          action: baseData.action,
          label: baseData.label,
          transport: baseData.transport,
        };

        elements.forEach((e) => setupElementGA(e, eventData));
      } else if (!querySelectorEvents[querySelector].optional_element) {
        // If we're on the right page, but the event's query selector
        // does not result in any elements, that's a bug and should
        // log an error so we can fix that.
        console.error(`cannot find ${querySelector}`);
      }
    });

    // bind GA events that have special conditions

    // tracks when MSS accordion on product page is expanded
    if (document.querySelector(`#view-product-page`)) {
      bindCheckboxCheckedGA("#view-product-page #mss-accordion-toggle", {
        event: `security_expand_accordion_tap`,
        category: `product`,
        action: `security expand accordion tap`,
        label: `detail view for MSS on for ${productName}`,
      });
    }

    if (document.querySelector(`body.catalog`)) {
      bindCheckboxCheckedGA("body.catalog #product-filter-pni-toggle", {
        event: `ding_checkbox_checked`,
        category: `buyersguide`,
        action: `ding checkbox checked`,
        label: `ding checkbox checked on ${pageTitle}`,
      });
    }

    trackSearchBoxUsage();
    trackGoBackToAllProductsLink();
  },
};

export default ProductGA;
