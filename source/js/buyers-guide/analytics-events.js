import { ReactGA, GoogleAnalytics } from "../common";

function getQuerySelectorEvents(pageTitle, productName) {
  return {
    // "site-wide" events
    "#donate-button": {
      category: `buyersguide`,
      action: `donate tap`,
      label: `${pageTitle} donate header`
    },
    "#donate-header-btn": {
      category: `buyersguide`,
      action: `donate tap`,
      label: `${pageTitle} donate header`
    },
    ".donate-banner a.btn.btn-secondary": {
      category: `buyersguide`,
      action: `donate tap`,
      label: `${pageTitle} donate footer`
    },

    // product events
    "#product-company-url": {
      category: `product`,
      action: `company link tap`,
      label: `company link for ${productName}`,
      transport: `beacon`
    },
    "#product-copy-link-button": {
      category: `product`,
      action: `copy link tap`,
      label: `copy link ${productName}`
    },
    "#product-live-chat": {
      category: `product`,
      action: `customer support link tap`,
      label: `support link for ${productName}`
    },
    "#creep-vote-btn": {
      category: `product`,
      action: `opinion submitted`,
      label: `opinion on ${productName}`
    },
    "a.privacy-policy-link": {
      category: `product`,
      action: `privacy policy link tap`,
      label: `policy link for ${productName}`,
      transport: `beacon`
    },

    // product updates
    ".product-update-link": {
      category: `product`,
      action: `update article link tap`,
      label: `update article link for ${productName}`,
      transport: `beacon`,
      optional: true
    }
  };
}

function setupElementGA(element, eventData) {
  element.onclick = () => {
    ReactGA.event(eventData);
  };
}

const ProductGA = {
  init: () => {
    if (GoogleAnalytics.doNotTrack) {
      // explicit check on DNT left in, to prevent
      // a whole heap of code from executing.
      return;
    }

    let productBox = document.querySelector(`.product-detail .h1-heading`);
    let productName = productBox ? productBox.textContent : `unknown product`;
    let pageTitle = document
      .querySelector(`meta[property='og:title']`)
      .getAttribute(`content`);
    let querySelectorEvents = getQuerySelectorEvents(pageTitle, productName);

    Object.keys(querySelectorEvents).forEach(querySelector => {
      let elements = document.querySelectorAll(querySelector);

      if (elements.length > 0) {
        let eventData = querySelectorEvents[querySelector];

        elements.forEach(e => setupElementGA(e, eventData));
      } else if (!querySelectorEvents[querySelector].optional) {
        console.error(`cannot find ${querySelector}`);
      }
    });
  }
};

export default ProductGA;
