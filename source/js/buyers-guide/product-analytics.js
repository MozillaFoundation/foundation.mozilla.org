import ReactGA from 'react-ga';

export default {
  init: () => {
    let productBox = document.querySelector(`.product-detail .h1-heading`);
    let productTitle = productBox ? productBox.textContent : `unknown product`;

    let productLiveChat = document.querySelector(`#product-live-chat`);

    if (productLiveChat) {
      productLiveChat.onclick = () => {
        ReactGA.event({
          category: `product`,
          action: `customer support link tap`,
          label: `support link for ${productTitle}`
        });
      };
    }
  }
};
