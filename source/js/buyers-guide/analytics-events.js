import { ReactGA, GoogleAnalytics } from "../common";

function getQuerySelectorEvents(pageTitle, productName) {
  return {
    // "site-wide" events
    "#donate-header-btn": {
      category: `buyersguide`,
      action: `donate tap`,
      label: `${pageTitle} donate header`,
    },
    ".donate-banner a.tw-btn-secondary": {
      category: `buyersguide`,
      action: `donate tap`,
      label: `${pageTitle} donate footer`,
    },

    // product events
    "#product-company-url": {
      category: `product`,
      action: `company link tap`,
      label: `company link for ${productName}`,
      transport: `beacon`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
    },
    "#product-live-chat": {
      category: `product`,
      action: `customer support link tap`,
      label: `support link for ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
      // Not all products have live-chat
      optional_element: true,
    },
    "#product-email": {
      category: `product`,
      action: `email link tap`,
      label: `email link for ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
      // Not all products have email
      optional_element: true,
    },
    "#product-twitter": {
      category: `product`,
      action: `twitter link tap`,
      label: `twitter link for ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
      // Not all products have Twitter
      optional_element: true,
    },
    "#creep-vote-btn": {
      category: `product`,
      action: `opinion submitted`,
      label: `opinion on ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
    },
    "a.privacy-policy-link": {
      category: `product`,
      action: `privacy policy link tap`,
      label: `policy link for ${productName}`,
      transport: `beacon`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
    },
    ".product-update-link": {
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
      category: `product`,
      action: `minimum security standards link tap`,
      label: `mss link for ${productName}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `#view-product-page`,
    },
    ".btn-recommend": {
      category: `buyersguide`,
      action: `submit a product button tap`,
      label: `submit a product button tap on ${pageTitle}`,
      // Custom properties (not sent to GA)
      conditionalQuery: `.btn-recommend`,
    },
  };
}

function setupElementGA(element, eventData) {
  element.addEventListener("click", () => ReactGA.event(eventData), true);
}

// tracks only when users tick off the checkbox (and not when they uncheck it)
function bindCheckboxCheckedGA(selector, eventMeta) {
  const checkbox = document.querySelector(selector);

  if (!checkbox) {
    console.error(`cannot find ${selector}`);
    return;
  }

  checkbox.addEventListener(
    "change",
    () => {
      if (checkbox.checked) {
        ReactGA.event(eventMeta);
      }
    },
    true
  );
}

function trackSearchBoxUsage() {
  const SESSION_KEY = `searchBoxUsed`;
  const searchBox = document.querySelector(
    "body.catalog #product-filter-search-input"
  );

  if (!searchBox) {
    console.error(`cannot find ${selector}`);
    return;
  }

  searchBox.addEventListener(
    "keydown",
    () => {
      let searchBoxUsed = sessionStorage.getItem(SESSION_KEY);

      if (!searchBoxUsed) {
        ReactGA.event({
          category: `buyersguide`,
          action: `type in search box`,
          label: `search box used`,
        });
      }

      sessionStorage.setItem(SESSION_KEY, true);
    },
    true
  );

  // window.addEventListener("beforeunload", (event) => {
  //   console.log(`>>> beforeunload: ${window.location}`);
  // });
}

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
      ReactGA.event({
        category: `buyersguide`,
        action: `product not found All link tap`,
        label: `All link tap for ${searchBox.value}`,
      });
    },
    true
  );
}

const ProductGA = {
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
        category: `product`,
        action: `security expand accordion tap`,
        label: `detail view for MSS on for ${productName}`,
      });
    }

    if (document.querySelector(`body.catalog`)) {
      bindCheckboxCheckedGA("body.catalog #product-filter-pni-toggle", {
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
