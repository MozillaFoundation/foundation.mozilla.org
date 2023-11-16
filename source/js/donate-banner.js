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

    // skip the banner if it got dismissed by the user today already
    if (!hideBanner && banner) {
      banner.classList.remove(`tw-hidden`);
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

      document.querySelector(`.wrapper`).animate(
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
        banner.classList.add(`tw-hidden`);
        this.setDismissDate();
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
