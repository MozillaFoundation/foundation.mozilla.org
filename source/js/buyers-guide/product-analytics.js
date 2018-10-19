import ReactGA from 'react-ga';

export default {
  init: () => {
    let productBox = document.querySelector(`.product-detail .h1-heading`);
    let productName = productBox ? productBox.textContent : `unknown product`;

    let productLiveChat = document.querySelector(`#product-live-chat`);
    let siteSocialButtonFacebook = document.querySelector(`#nav-social-button-fb`);
    let siteSocialButtonTwitter = document.querySelector(`#nav-social-button-twitter`);
    let siteSocialButtonEmail = document.querySelector(`#nav-social-button-email`);
    let siteCopyLink = document.querySelector(`#nav-social-button-link`);
    let productCopyLink = document.querySelector(`#product-copy-link-button`);
    let voteForm = document.querySelector(`#creep-vote`);
    let productSocialButtonFacebook = document.querySelector(`#product-social-button-fb`);
    let productSocialButtonTwitter = document.querySelector(`#product-social-button-twitter`);
    let productSocialButtonEmail = document.querySelector(`#product-social-button-email`);
    let donateButton = document.querySelector(`#donate-button`);

    if (productLiveChat) {
      productLiveChat.onclick = () => {
        ReactGA.event({
          category: `product`,
          action: `customer support link tap`,
          label: `support link for ${productName}`
        });
      };
    }

    if (donateButton) {
      donateButton.onclick = () => {
        let pageTitle = document.querySelector(`meta[property='og:title']`).getAttribute(`content`);

        ReactGA.event({
          category: `site`,
          action: `donate tap`,
          label: `${pageTitle} donate header`
        });
      };
    }

    if (siteSocialButtonFacebook) {
      siteSocialButtonFacebook.onclick = () => {
        ReactGA.event({
          category: `site`,
          action: `share tap`,
          label: `share site to Facebook`,
          transport: `beacon`
        });
      };
    }

    if (siteSocialButtonTwitter) {
      siteSocialButtonTwitter.onclick = () => {
        ReactGA.event({
          category: `site`,
          action: `share tap`,
          label: `share site to Twitter`,
          transport: `beacon`
        });
      };
    }

    if (siteCopyLink) {
      siteCopyLink.onclick = () => {
        ReactGA.event({
          category: `site`,
          action: `copy link tap`,
          label: `copy link to site `
        });
      };
    }

    if (siteSocialButtonEmail) {
      siteSocialButtonEmail.onclick = () => {
        ReactGA.event({
          category: `site`,
          action: `share tap`,
          label: `share site to Email`,
          transport: `beacon`
        });
      };
    }

    if (productCopyLink) {
      productCopyLink.onclick = () => {
        ReactGA.event({
          category: `product`,
          action: `copy link tap`,
          label: `copy link ${productName}`
        });
      };
    }

    if (voteForm) {
      voteForm.onsubmit = () => {
        ReactGA.event({
          category: `product`,
          action: `opinion submitted`,
          label: `opinion on ${productName}`
        });
      };
    }

    if (productSocialButtonFacebook) {
      productSocialButtonFacebook.onclick = () => {
        ReactGA.event({
          category: `product`,
          action: `share tap`,
          label: `share ${productName} to Facebook`,
          transport: `beacon`
        });
      };
    }

    if (productSocialButtonTwitter) {
      productSocialButtonTwitter.onclick = () => {
        ReactGA.event({
          category: `product`,
          action: `share tap`,
          label: `share ${productName} to Twitter`,
          transport: `beacon`
        });
      };
    }

    if (productSocialButtonEmail) {
      productSocialButtonEmail.onclick = () => {
        ReactGA.event({
          category: `product`,
          action: `share tap`,
          label: `share ${productName} to Email`,
          transport: `beacon`
        });
      };
    }
  }
};
