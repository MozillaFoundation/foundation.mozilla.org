import { ReactGA } from "../../../../common";

/**
 * Bind handler to social buttons on MozFest footer
 */
export default () => {
  document
    .querySelectorAll(`body.mozfest footer a[data-platform]`)
    .forEach(button => {
      button.addEventListener(`click`, () => {
        ReactGA.event({
          category: `social`,
          action: `social button tap`,
          label: `${button.dataset.platform} footer button tap`
        });
      });
    });
};
