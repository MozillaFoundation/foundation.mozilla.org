/**
 * Bind handler to window for sticky CTA button to work on mobile
 */
export default () => {
  let lastKnownScrollPosition = 0;
  let ticking = false;
  let elBurgerWrapper = document.querySelector(`.wrapper-burger`);

  let adjustNavbar = (scrollPosition) => {
    if (scrollPosition > 0) {
      elBurgerWrapper.classList.add(`scrolled`);
    } else {
      elBurgerWrapper.classList.remove(`scrolled`);
    }
  };

  let elCtaAnchor = document.querySelector(`#cta-anchor`);
  let noopCtaButton = () => {};
  let adjustCtaButton = noopCtaButton;
  // Set elStickyButton to a noop object if on MozFest site
  // This is to address a bug when the sticky button is blocking users to access full content on Tito popup
  // See https://github.com/MozillaFoundation/foundation.mozilla.org/issues/10307
  let elStickyButton = new URL(window.location.href).searchParams.has("tito")
    ? {
        classList: {
          add: function () {},
          remove: function () {},
        },
      }
    : document.querySelector(`.narrow-sticky-button-container`);

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

    let scrollCtaButton = (scrollPosition) => {
      if (scrollPosition > positionToHideButton) {
        elStickyButton.classList.add(`hidden`);
        adjustCtaButton = noopCtaButton;
      }
    };

    let initCtaButton = (scrollPosition) => {
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
