import injectJoinUs from "./join-us.js";
import injectPetition from "./petition.js";
import injectPetitionThankYou from "./petition-thank-you.js";

/**
 * Inject React components
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 * @param {String} siteUrl Foundation site base URL
 */
export const injectCommonReactComponents = (apps, siteUrl) => {
  injectJoinUs(apps, siteUrl);
  // Current petition form and thank you screen
  injectPetition(apps, siteUrl);
  // FormAssembly petition thank you screen
  injectPetitionThankYou(apps);
};
