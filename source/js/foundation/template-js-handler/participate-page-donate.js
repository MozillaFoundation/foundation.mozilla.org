/**
 * Bind click handler to "#view-participate .card-cta .btn[href*="donate.mozilla.org"]"
 * (the Donate CTA button on participate page)
 */
export default () => {
  let participateDonateBtn = document.querySelector(
    `#view-participate .card-cta .btn[href*="donate.mozilla.org"]`
  );

  if (participateDonateBtn) {
    participateDonateBtn.addEventListener(`click`, () => {
      window.dataLayer.push({
        event: `donate_button_tap_participate_page`,
        category: `donate`,
        action: `donate button tap`,
        label: document.title,
      });
    });
  }
};
