/**
 * Initiate primary nav scripts
 * @param {String} siteUrl Foundation site base URL
 * @param {Object} primaryNavModule primary nav module to initiate
 */
export const initializePrimaryNav = (siteUrl, primaryNavModule) => {
  if (primaryNavModule) {
    primaryNavModule.init();
  }
};
