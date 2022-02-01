import { ReactGA } from "../../../../../common";

/**
 * Bind handler to download button for Firefox/Chrome download button
 * on the youtube regrets page.
 */

export default () => {
  const regretsReporter = document.querySelector(
    `#view-youtube-regrets-reporter`
  );

  const addGATracking = (elements, browserName) => {
    elements.forEach((button) => {
      const location = button.dataset.location
        ? ` ${button.dataset.location}`
        : ``;

      button.addEventListener(`click`, () => {
        ReactGA.event({
          category: `CTA download`,
          action: `${browserName}${location} button tap`,
          label: `${document.title} - ${button.innerText}`,
          transport: `beacon`,
        });
      });
    });
  };

  addGATracking(
    regretsReporter.querySelectorAll(`.btn-download.btn-firefox-download`),
    `Firefox`
  );

  addGATracking(
    regretsReporter.querySelectorAll(`.btn-download.btn-chrome-download`),
    `Chrome`
  );
};
