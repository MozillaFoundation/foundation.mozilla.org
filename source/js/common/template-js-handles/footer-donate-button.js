import { ReactGA } from "../react-ga-proxy.js";

/**
 * Bind click handler to #donate-footer-btn
 * ("Donate" button on footer)
 */
export default () => {
  let donateFooterBtn = document.getElementById(`donate-footer-btn`);

  if (donateFooterBtn) {
    donateFooterBtn.addEventListener(`click`, () => {
      ReactGA.event({
        category: `donate`,
        action: `donate button tap`,
        label: `${document.title} footer`,
      });
    });
  }
};
