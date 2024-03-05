import { ReactGA } from "../../common";

/**
 * Bind click handler to data-donate-header-button
 * ("Donate" button on primary nav)
 */
export default () => {
  const donateHeaderBtn = document.querySelectorAll(
    "[data-donate-header-button]"
  );
  if (donateHeaderBtn.length > 0) {
    donateHeaderBtn.forEach((element) => {
      element.addEventListener(`click`, () => {
        ReactGA.event({
          category: `donate`,
          action: `donate button tap`,
          label: `${document.title} header`,
        });
      });
    });
  }
};
