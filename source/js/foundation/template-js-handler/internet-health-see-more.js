/**
 * Bind click handler to "#see-more-modular-page"
 */
export default () => {
  let seeMorePage = document.querySelector(`#see-more-modular-page`);

  if (seeMorePage) {
    let label = ``;
    let pageHeader = document.querySelector(`.cms h1`);

    if (pageHeader) {
      label = `${pageHeader.innerText} - footer cta`;
    }

    seeMorePage.addEventListener(`click`, () => {
      ReactGA.event({
        category: `navigation`,
        action: `page footer cta`,
        label: label
      });
    });
  }
};
