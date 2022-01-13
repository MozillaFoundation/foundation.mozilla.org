import injectMultipageNav from "./multipage-nav.js";
import injectNews from "./news.js";
import injectPetition from "./petition.js";
import injectPulseProjectList from "./pulse-project-list.js";
import injectShareButtonGroup from "./share-button-group.js";
import injectPulseTabbedProfileDirectory from "./pulse-tabbed-profile-filters";

/**
 * Inject React components
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 * @param {String} siteUrl Foundation site base URL
 * @param {Object} env Object of environment variables
 */
export const injectReactComponents = (apps, siteUrl, env) => {
  injectMultipageNav(apps);
  injectNews(apps, env);
  injectPetition(apps, siteUrl);
  injectPulseProjectList(apps, env);
  injectShareButtonGroup(apps);
  injectPulseTabbedProfileDirectory(apps);
};
