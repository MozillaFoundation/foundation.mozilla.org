import { ReactGA } from "../../common";

/**
 * Bind handler to social buttons on MozFest footer
 */
export default () => {
  let footerSocialButtons = document.querySelectorAll(
    `body.mozfest footer a[data-platform]`
  );

  if (footerSocialButtons) {
    footerSocialButtons.forEach(button => {
      button.addEventListener(`click`, () => {
        ReactGA.event({
          category: `social`,
          action: `social button tap`,
          label: `${button.dataset.platform} footer button tap`
        });
      });
    });
  }
};
