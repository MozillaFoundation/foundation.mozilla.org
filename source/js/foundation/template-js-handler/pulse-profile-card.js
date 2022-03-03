import { ReactGA } from "../../common";

/**
 * Bind handlers to elements in ".profiles .person-card"
 */
export default () => {
  //Profile Directory Cards Social Media GA

  function profileCardSocialAnalytics(
    socialTwitter,
    socialLinkedIn,
    profileName
  ) {
    if (socialTwitter) {
      socialTwitter.addEventListener(`click`, () => {
        ReactGA.event({
          category: `profiles`,
          action: `profile tap`,
          label: `${document.title} ${profileName} twitter`,
          transport: `beacon`,
        });
      });
    }

    if (socialLinkedIn) {
      socialLinkedIn.addEventListener(`click`, () => {
        ReactGA.event({
          category: `profiles`,
          action: `profile tap`,
          label: `${document.title} ${profileName} linkedin`,
          transport: `beacon`,
        });
      });
    }
  }

  //Profile Directory Card Headshot/Name GA

  function bindProfileCardAnalytics(profileCards) {
    // event listener & GA
    let bindAnalytics = (element, profileName) => {
      element.addEventListener(`click`, () => {
        ReactGA.event({
          category: `profiles`,
          action: `profile tap`,
          label: `${document.title} ${profileName} pulse profile`,
          transport: `beacon`,
        });
      });
    };

    // adding event listener for each headshot & name
    profileCards.forEach((card) => {
      let profileHeadshotElement = card.querySelector(`.headshot-container`);
      let profileNameElement = card.querySelector(`.meta-block-name`);
      let profileName = profileNameElement?.textContent.trim();

      [(profileNameElement, profileHeadshotElement)].forEach((target) =>
        bindAnalytics(target, profileName)
      );

      let socialTwitter = card.querySelector(`.twitter`);
      let socialLinkedIn = card.querySelector(`.linkedIn`);
      profileCardSocialAnalytics(socialTwitter, socialLinkedIn, profileName);
    });
  }

  // store profile cards
  function updateProfileList() {
    let profileCards = document.querySelectorAll(`.profiles .person-card`);
    bindProfileCardAnalytics(profileCards);
  }

  // Checks for profile cards in the initial page load
  updateProfileList();

  // And start listening for profile filter events,
  // in case profile cards get updated.
  document.addEventListener(`profiles:list-updated`, () => updateProfileList());
};
