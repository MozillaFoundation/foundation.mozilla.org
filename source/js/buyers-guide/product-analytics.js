import ReactGA from 'react-ga';

function getElementGAInformation(pageTitle, productName) {
  return {
    'product-live-chat': {
      category: `product`,
      action: `customer support link tap`,
      label: `support link for ${productName}`
    },
    'donate-button': {
      category: `site`,
      action: `donate tap`,
      label: `${pageTitle} donate header`
    },
    'donate-button-main': {
      category: `site`,
      action: `donate tap`,
      label: `${pageTitle} donate header`
    },
    'donate-button-footer': {
      category: `site`,
      action: `donate tap`,
      label: `${pageTitle} donate footer`
    },
    'nav-social-button-fb': {
      category: `site`,
      action: `share tap`,
      label: `share site to Facebook`,
      transport: `beacon`
    },
    'nav-social-button-twitter': {
      category: `site`,
      action: `share tap`,
      label: `share site to Twitter`,
      transport: `beacon`
    },
    'nav-social-button-link': {
      category: `site`,
      action: `copy link tap`,
      label: `copy link to site `
    },
    'nav-social-button-email': {
      category: `site`,
      action: `share tap`,
      label: `share site to Email`,
      transport: `beacon`
    },
    'nav-social-button-fb-mb': {
      category: `site`,
      action: `share tap`,
      label: `share site to Facebook`,
      transport: `beacon`
    },
    'nav-social-button-twitter-mb': {
      category: `site`,
      action: `share tap`,
      label: `share site to Twitter`,
      transport: `beacon`
    },
    'nav-social-button-link-mb': {
      category: `site`,
      action: `copy link tap`,
      label: `copy link to site `
    },
    'nav-social-button-email-mb': {
      category: `site`,
      action: `share tap`,
      label: `share site to Email`,
      transport: `beacon`
    },
    'product-copy-link-button': {
      category: `product`,
      action: `copy link tap`,
      label: `copy link ${productName}`
    },
    'creep-vote-btn': {
      category: `product`,
      action: `opinion submitted`,
      label: `opinion on ${productName}`
    },
    'product-social-button-fb': {
      category: `product`,
      action: `share tap`,
      label: `share ${productName} to Facebook`,
      transport: `beacon`
    },
    'product-social-button-twitter': {
      category: `product`,
      action: `share tap`,
      label: `share ${productName} to Twitter`,
      transport: `beacon`
    },
    'product-social-button-email': {
      category: `product`,
      action: `share tap`,
      label: `share ${productName} to Email`,
      transport: `beacon`
    }
  };
}

function setupElementGA(elementId, opts) {
  let element = document.getElementById(elementId);

  if (element) {
    element.onclick = () => {
      ReactGA.event(opts);
    };
  }
}

const ProductGA = {
  init: () => {
    let productBox = document.querySelector(`.product-detail .h1-heading`);
    let productName = productBox ? productBox.textContent : `unknown product`;
    let pageTitle = document.querySelector(`meta[property='og:title']`).getAttribute(`content`);
    let elementsWithAnalytics = getElementGAInformation(pageTitle, productName);

    Object.keys(elementsWithAnalytics).forEach( elementId => {
      setupElementGA(elementId, elementsWithAnalytics[elementId]);
    });
  }
};

export default ProductGA;
