import { ReactGA } from "../../common";
import copyToClipboard from "../../copy-to-clipboard";

export default () => {
  const shareButtonGroups = document.querySelectorAll(
    ".share-button-group-wrapper"
  );

  if (!shareButtonGroups) {
    return;
  }

  let bindGaEvent = (type = ``) => {
    ReactGA.event({
      category: `social`,
      action: `${type} share tap`,
      label: `${type} share`,
      transport: `beacon`,
    });
  };

  let linkButtonClick = (event) => {
    event.preventDefault();
    const linkButton = event.target;

    linkButton.classList.add("copied");
    linkButton.title = "Copied";
    linkButton.querySelector("span").innerText = "Copied"

    copyToClipboard(event.target, window.location.href);
    bindGaEvent("link");
  };

  shareButtonGroups.forEach((shareButtonGroup) => {
    const facebookButton = shareButtonGroup.querySelector(".facebook-share");
    const twitterButton = shareButtonGroup.querySelector(".facebook-share");
    const emailButton = shareButtonGroup.querySelector(".email-share");
    const linkButton = shareButtonGroup.querySelector(".link-share");

    facebookButton.addEventListener(`click`, () => {
      bindGaEvent("facebook");
    });
    twitterButton.addEventListener(`click`, () => {
      bindGaEvent("twitter");
    });
    emailButton.addEventListener(`click`, () => {
      bindGaEvent("email");
    });
    linkButton.addEventListener(`click`, (event) => {
      linkButtonClick(event);
    });
  });
};
