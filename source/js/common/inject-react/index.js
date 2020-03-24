import injectJoinUs from "./join-us.js";

/**
 * Inject React components
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 * @param {String} siteUrl Foundation site base URL
 * @param {String} csrfToken CSRF Token
 */
export const injectReactComponents = (apps, siteUrl, csrfToken) => {
  injectJoinUs(apps, siteUrl, csrfToken);
};
