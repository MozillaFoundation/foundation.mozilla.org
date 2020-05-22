import navNewsletter from "../nav-newsletter.js";

/**
 * Initiate primary nav scripts
 * @param {String} siteUrl Foundation site base URL
 * @param {String} csrfToken CSRF Token
 * @param {Object} primaryNavModule primary nav module to initiate
 */
export const initializePrimaryNav = (siteUrl, csrfToken, primaryNavModule) => {
  if (primaryNavModule) {
    primaryNavModule.init();
  }
  navNewsletter.init(siteUrl, csrfToken);
};
