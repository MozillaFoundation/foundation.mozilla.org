import ReactGA from "./react-ga-proxy.js";

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

  // TODO:FIXME:
  // The proposals page is created via CMS and so are these buttons.
  // Not sure what the best way is to target these buttons.
  let beginSessionProposalButtons = document.querySelectorAll(
    `body.mozfest a.btn.btn-primary[href='https://forms.gle/WY2zCp6cfdJU2fmp7']`
  );

  if (beginSessionProposalButtons) {
    beginSessionProposalButtons.forEach(button => {
      button.addEventListener(`click`, () => {
        ReactGA.event({
          category: `CTA`,
          action: `submit proposal tap`,
          label: `proposal button tap`
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
