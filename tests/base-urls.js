const LEGACY_FOUNDATION_DOMAIN = "http://legacy.localhost:8000";

module.exports = {
  donateBaseUrl: function (locale = "en") {
    return `${LEGACY_FOUNDATION_DOMAIN}/${locale}/donate`;
  },
  foundationDomain: LEGACY_FOUNDATION_DOMAIN,
  foundationBaseUrl: function (locale = "en") {
    return `${LEGACY_FOUNDATION_DOMAIN}/${locale}`;
  },
  mozfestBaseUrl: function (locale = "en") {
    return `http://mozfest.localhost:8000/${locale}`;
  },
  pniBaseUrl: function (locale = "en") {
    return `${LEGACY_FOUNDATION_DOMAIN}/${locale}/privacynotincluded`;
  },
};
