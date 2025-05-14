/**
 * Bind handler to primary buttons on MozFest
 */
export default () => {
  document
    .querySelectorAll(`body.mozfest .cms a.tw-btn-primary`)
    .forEach((button) => {
      button.addEventListener(`click`, () => {
        window.dataLayer.push({
          event: `cta_button_tap`,
          category: `CTA`,
          action: `button tap`,
          label: button.innerText,
        });
      });
    });
};
