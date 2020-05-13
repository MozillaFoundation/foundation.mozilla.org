/**
 * Bind handler to window for sticky CTA button to work on mobile
 */
export default () => {
  let lastKnownScrollPosition = 0;
  let ticking = false;
  let elBurgerWrapper = document.querySelector(`.wrapper-burger`);

  let adjustNavbar = scrollPosition => {
    if (scrollPosition > 0) {
      elBurgerWrapper.classList.add(`scrolled`);
    } else {
      elBurgerWrapper.classList.remove(`scrolled`);
    }
  };

  let elCtaAnchor = document.querySelector(`#cta-anchor`);
  let elStickyButton = document.querySelector(
    `.narrow-sticky-button-container`
  );
  let noopCtaButton = () => {};
  let adjustCtaButton = noopCtaButton;

  if (elCtaAnchor && elStickyButton) {
    let getAnchorPosition = () => {
      return (
        elCtaAnchor.getBoundingClientRect().top +
        window.scrollY -
        window.innerHeight
      );
    };

    let ctaAnchorPosition = getAnchorPosition();

    window.addEventListener(`resize`, () => {
      ctaAnchorPosition = getAnchorPosition();
    });

    let bufferOffset = window.innerHeight / 2;
    let positionToHideButton = ctaAnchorPosition + bufferOffset;

    let scrollCtaButton = scrollPosition => {
      if (scrollPosition > positionToHideButton) {
        elStickyButton.classList.add(`hidden`);
        adjustCtaButton = noopCtaButton;
      }
    };

    let initCtaButton = scrollPosition => {
      if (scrollPosition <= positionToHideButton) {
        elStickyButton.classList.remove(`hidden`);
        adjustCtaButton = scrollCtaButton;
      }
    };

    adjustCtaButton = initCtaButton;
  }

  let onScroll = () => {
    lastKnownScrollPosition = window.scrollY;

    if (!ticking) {
      window.requestAnimationFrame(() => {
        adjustNavbar(lastKnownScrollPosition);
        adjustCtaButton(lastKnownScrollPosition);
        ticking = false;
      });
    }

    ticking = true;
  };

  window.addEventListener(`scroll`, onScroll);

  // Call once to get scroll position on initial page load.
  onScroll();
};
