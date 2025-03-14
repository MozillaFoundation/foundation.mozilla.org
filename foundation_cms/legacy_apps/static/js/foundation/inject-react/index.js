import injectPulseProjectList from "./pulse-project-list.js";
import injectPulseTabbedProfileDirectory from "./pulse-tabbed-profile-filters";

/**
 * Inject React components
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 * @param {String} siteUrl Foundation site base URL
 * @param {Object} env Object of environment variables
 */
export const injectReactComponents = (apps, siteUrl, env) => {
  injectPulseProjectList(apps, env);
  injectPulseTabbedProfileDirectory(apps);
};
