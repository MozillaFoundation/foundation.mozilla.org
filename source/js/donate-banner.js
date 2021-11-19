const DonateBanner = {
  init: function () {
    const today = new Date();
    const DISMISS_KEY = "donate banner dismiss day";
    const banner = document.querySelector(`.donate-banner`);
    const hideBanner =
      parseInt(localStorage.getItem(DISMISS_KEY)) === today.getDay();
    const closeButton = hideBanner
      ? undefined
      : banner?.querySelector(`a.banner-close`);

    // skip the banner if it got dismissed by the user today already
    if (!hideBanner && banner) {
      banner.classList.remove(`tw-hidden`);
    }

    closeButton?.addEventListener(`click`, (e) => {
      e.preventDefault();

      localStorage.removeItem(DISMISS_KEY);

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
        localStorage.setItem(DISMISS_KEY, today.getDay());
      };
    });
  },
};

export default DonateBanner;
