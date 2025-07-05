/**
 * Open/Close functionality for the Donate banner that slides from the top of the page.
 */

const DonateBanner = {
  DISMISS_KEY: "donate banner dismiss day",
  init: function () {
    const banner = document.querySelector(`.donate-banner`);
    const hideBanner = this.shouldHideBanner();
    const closeButton = hideBanner
      ? undefined
      : banner?.querySelector(`a.banner-close`);
    const ctaButton = banner?.querySelector(`#banner-cta-button`);
    const wrapper =
      document.querySelector(`.wrapper`) ||
      document.querySelector(`.primary-nav-container-wrapper`);

    // skip the banner if it got dismissed by the user today already
    if (hideBanner) {
      // remove the banner from the DOM to prevent it
      // from creating unexpected behavior due to its absolute positioning.
      banner.remove();
      return;
    }

    if (!hideBanner && banner) {
      banner.classList.remove(`tw-hidden`);
    }

    if (window.wagtailAbTesting) {
      ctaButton?.addEventListener(`click`, (e) => {
        wagtailAbTesting.triggerEvent("donate-banner-link-click");
      });
    }

    closeButton?.addEventListener(`click`, (e) => {
      e.preventDefault();

      banner.style.position = "absolute";
      banner.style.top = "0px";

      const animationOptions = {
        // timing options
        duration: 300,
        fill: "forwards",
        easing: "ease-in",
      };

      wrapper.animate(
        [
          // keyframes
          {
            marginTop:
              document.querySelector(`.donate-banner`).clientHeight + `px`,
          },
          {
            marginTop: 0,
          },
        ],
        animationOptions
      );

      const closeAnimation = banner.animate(
        [
          // keyframes
          {
            transform: `translateY(0)`,
          },
          {
            transform: `translateY(-100%)`,
          },
        ],
        animationOptions
      );

      closeAnimation.onfinish = () => {
        this.setDismissDate();

        // The banner will not reappear after the user has dismissed it until the next day.
        // We might as well remove it from the DOM to prevent it
        // from creating unexpected behavior due to its absolute positioning.
        banner.remove();
      };
    });
  },
  getDismissDate() {
    return localStorage.getItem(this.DISMISS_KEY);
  },
  setDismissDate() {
    const today = new Date();
    localStorage.setItem(this.DISMISS_KEY, today.toDateString()); // e.g., Thu Nov 09 2023
  },
  shouldHideBanner() {
    const today = new Date();

    return this.getDismissDate() === today.toDateString();
  },
};

export default DonateBanner;
