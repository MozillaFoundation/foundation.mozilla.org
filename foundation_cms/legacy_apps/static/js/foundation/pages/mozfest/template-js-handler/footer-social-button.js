/**
 * Bind handler to social buttons on MozFest footer
 */
export default () => {
  document
    .querySelectorAll(`body.mozfest footer a[data-platform]`)
    .forEach((button) => {
      button.addEventListener(`click`, () => {
        window.dataLayer.push({
          event: `footer_social_button_tap`,
          category: `social`,
          action: `social button tap`,
          label: `${button.dataset.platform} footer button tap`,
        });
      });
    });
};
