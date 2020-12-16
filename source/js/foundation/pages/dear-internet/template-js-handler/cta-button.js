import { ReactGA } from "../../../../common";

/**
 * Bind handler to CTA button on Dear Internet page
 */
export default () => {
  const ctaButton = document.querySelector(`#view-dear-internet .cta .btn`);

  if (!ctaButton) return;

  ctaButton.addEventListener(`click`, () => {
    ReactGA.event({
      category: `donate`,
      action: `donate button tap`,
      label: `main CTA`,
      transport: `beacon`,
    });
  });
};
