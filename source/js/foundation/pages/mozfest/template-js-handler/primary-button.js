import { ReactGA } from "../../../../common";

/**
 * Bind handler to primary buttons on MozFest
 */
export default () => {
  document
    .querySelectorAll(`body.mozfest .cms a.tw-btn-primary`)
    .forEach((button) => {
      button.addEventListener(`click`, () => {
        ReactGA.event({
          category: `CTA`,
          action: `button tap`,
          label: button.innerText,
        });
      });
    });
};
