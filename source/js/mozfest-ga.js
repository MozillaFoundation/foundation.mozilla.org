import ReactGA from "./common/react-ga-proxy.js";

const bindMozfestGAEventTrackers = () => {
  let homeWatchVideoButton = document.querySelector(
    `#mozfest-home-watch-video-button`
  );

  if (homeWatchVideoButton) {
    homeWatchVideoButton.addEventListener(`click`, () => {
      ReactGA.event({
        category: `CTA`,
        action: `watch video tap`,
        label: `watch video button tap`
      });
    });
  }

  let cmsPrimaryButtons = document.querySelectorAll(
    `body.mozfest .cms a.btn.btn-primary`
  );

  if (cmsPrimaryButtons) {
    cmsPrimaryButtons.forEach(button => {
      button.addEventListener(`click`, () => {
        ReactGA.event({
          category: `CTA`,
          action: `button tap`,
          label: button.innerText
        });
      });
    });
  }

  let footerSocialButtons = document.querySelectorAll(
    `body.mozfest footer a[data-platform]`
  );

  if (footerSocialButtons) {
    footerSocialButtons.forEach(button => {
      button.addEventListener(`click`, () => {
        ReactGA.event({
          category: `social`,
          action: `social button tap`,
          label: `${button.dataset.platform} footer button tap`
        });
      });
    });
  }
};

export default bindMozfestGAEventTrackers;
