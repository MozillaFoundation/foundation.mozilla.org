const FOUNDATION_DOMAIN = "http://localhost:8000";

module.exports = {
  donateBaseUrl: function (locale = "en") {
    return `${FOUNDATION_DOMAIN}/${locale}/donate`;
  },
  foundationDomain: FOUNDATION_DOMAIN,
  foundationBaseUrl: function (locale = "en") {
    return `${FOUNDATION_DOMAIN}/${locale}`;
  },
  mozfestBaseUrl: function (locale = "en") {
    return `http://mozfest.localhost:8000/${locale}`;
  },
  pniBaseUrl: function (locale = "en") {
    return `${FOUNDATION_DOMAIN}/${locale}/privacynotincluded`;
  },
};
