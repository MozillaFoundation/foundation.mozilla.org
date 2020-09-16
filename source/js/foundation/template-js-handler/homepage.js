import { ReactGA } from "../../common";

/**
 * Bind click handler to "#see-more-modular-page" (the "see more" link in ih_cta.html)
 */
export default () => {
  const DOC_TITLE = document.title;

  let bindCtaGA = (element, eventAction) => {
    if (element) {
      element.addEventListener(`click`, () => {
        ReactGA.event({
          category: `CTA read more`,
          action: eventAction,
          label: `${DOC_TITLE} - ${element.innerText}`,
        });
      });
    }
  };

  // Hero CTA button
  bindCtaGA(
    document.querySelector(`#homepage-hero-cta`),
    `read more hero button tap`
  );

  // Cause Statement CTA link
  bindCtaGA(
    document.querySelector(`#homepage-cause-statement-cta`),
    `more about our work link tap`
  );

  // News You Can Use CTA link
  bindCtaGA(
    document.querySelector(`#news-you-can-use-cta`),
    `read news link tap`
  );

  // Partner CTA link
  bindCtaGA(
    document.querySelector(`#partner-cta`),
    `let's work together link tap`
  );

  // Donate Banner CTA
  let donateBannerCta = document.querySelector("#donate-banner-cta");
  if (donateBannerCta) {
    donateBannerCta.addEventListener(`click`, () => {
      ReactGA.event({
        category: `donate`,
        action: `donate button tap banner`,
        label: `${DOC_TITLE} banner`,
      });
    });
  }
};
