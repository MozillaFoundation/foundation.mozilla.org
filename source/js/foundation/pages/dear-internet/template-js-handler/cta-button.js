/**
 * Bind handler to CTA button on Dear Internet page
 */
export default () => {
  const ctaButton = document.querySelector(`#view-dear-internet .cta .btn`);

  if (!ctaButton) return;

  ctaButton.addEventListener(`click`, () => {
    window.dataLayer.push({
      event: `main_cta_donate_button_tap`,
      category: `donate`,
      action: `donate button tap`,
      label: `main CTA`,
      transport: `beacon`,
    });
  });
};
