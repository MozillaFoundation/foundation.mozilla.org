import { ReactGA } from "../../common";

/**
 * Bind click handler to #donate-header-btn
 * ("Donate" button on primary nav)
 */
export default () => {
  let donateHeaderBtn = document.getElementById(`donate-header-btn`);
  if (donateHeaderBtn) {
    donateHeaderBtn.addEventListener(`click`, () => {
      ReactGA.event({
        category: `donate`,
        action: `donate button tap`,
        label: `${document.title} header`,
      });
    });
  }
};
