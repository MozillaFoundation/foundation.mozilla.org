import ReactGA from './react-ga-proxy';
import DNT from './dnt.js';

function getQuerySelectorEvents(pageTitle, productName) {
  return {
    // "site-wide" events
    '#donate-button': {
      category: `buyersguide`,
      action: `donate tap`,
      label: `${pageTitle} donate header`
    },
    '#donate-button-main': {
      category: `buyersguide`,
      action: `donate tap`,
      label: `${pageTitle} donate header`
    },
    '#donate-button-footer': {
      category: `buyersguide`,
      action: `donate tap`,
      label: `${pageTitle} donate footer`
    },
    '#nav-social-button-fb': {
      category: `buyersguide`,
      action: `share tap`,
      label: `share site to Facebook`,
      transport: `beacon`
    },
    '#nav-social-button-twitter': {
      category: `buyersguide`,
      action: `share tap`,
      label: `share site to Twitter`,
      transport: `beacon`
    },
    '#nav-social-button-email': {
      category: `buyersguide`,
      action: `share tap`,
      label: `share site to Email`,
      transport: `beacon`
    },
    '#nav-social-button-fb-mb': {
      category: `buyersguide`,
      action: `share tap`,
      label: `share site to Facebook`,
      transport: `beacon`
    },
    '#nav-social-button-twitter-mb': {
      category: `buyersguide`,
      action: `share tap`,
      label: `share site to Twitter`,
      transport: `beacon`
    },
    '#nav-social-button-email-mb': {
      category: `buyersguide`,
      action: `share tap`,
      label: `share site to Email`,
      transport: `beacon`
    },

    // product events
    '#product-company-url': {
      category: `product`,
      action: `company link tap`,
      label: `company link for ${productName}`,
      transport: `beacon`
    },
    '#product-copy-link-button': {
      category: `product`,
      action: `copy link tap`,
      label: `copy link ${productName}`
    },
    '#product-live-chat': {
      category: `product`,
      action: `customer support link tap`,
      label: `support link for ${productName}`
    },
    '#creep-vote-btn': {
      category: `product`,
      action: `opinion submitted`,
      label: `opinion on ${productName}`
    },
    '#product-social-button-fb': {
      category: `product`,
      action: `share tap`,
      label: `share ${productName} to Facebook`,
      transport: `beacon`
    },
    '#product-social-button-twitter': {
      category: `product`,
      action: `share tap`,
      label: `share ${productName} to Twitter`,
      transport: `beacon`
    },
    '#product-social-button-email': {
      category: `product`,
      action: `share tap`,
      label: `share ${productName} to Email`,
      transport: `beacon`
    },
    '#privacy-policy-link': {
      category: `product`,
      action: `privacy policy link tap`,
      label: `policy link for ${productName}`,
      transport: `beacon`
    },
    '#reading-level-link': {
      category: `product`,
      action: `carnegie mellon reading level links`,
      label: `reading level link for ${productName}`,
      transport: `beacon`
    },

    // product updates
    '.product-update-link': {
      category: `product`,
      action: `update article link tap`,
      label: `update article link for ${productName}`,
      transport: `beacon`
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
    if (!DNT.allowTracking) {
      return;
    }

    let productBox = document.querySelector(`.product-detail .h1-heading`);
    let productName = productBox ? productBox.textContent : `unknown product`;
    let pageTitle = document.querySelector(`meta[property='og:title']`).getAttribute(`content`);
    let querySelectorEvents = getQuerySelectorEvents(pageTitle, productName);

    Object.keys(querySelectorEvents).forEach( querySelector => {
      let elements = document.querySelectorAll(querySelector);

      if (elements.length > 0) {
        let eventData = querySelectorEvents[querySelector];

        elements.forEach(e => setupElementGA(e, eventData));
      }
    });
  }
};

export default ProductGA;
