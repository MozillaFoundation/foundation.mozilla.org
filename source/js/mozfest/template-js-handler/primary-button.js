import { ReactGA } from "../../common";

/**
 * Bind handler to primary buttons on MozFest
 */
export default () => {
  let cmsPrimaryButtons = document.querySelectorAll(
    `body.mozfest .cms a.btn.btn-primary`
  );

  if (cmsPrimaryButtons) {
    cmsPrimaryButtons.forEach(button => {
      button.addEventListener(`click`, () => {
        ReactGA.event({
          category: `CTA`,
          action: `button tap`,
          label: button.innerText
        });
      });
    });
  }
};
