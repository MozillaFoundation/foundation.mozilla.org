module.exports = {
  donateBaseUrl: function (locale = "en") {
    return `http://localhost:8000/${locale}/donate`;
  },
  foundationBaseUrl: function (locale = "en") {
    return `http://localhost:8000/${locale}`;
  },
  mozfestBaseUrl: function (locale = "en") {
    return `http://mozfest.localhost:8000/${locale}`;
  },
  pniBaseUrl: function (locale = "en") {
    return `http://localhost:8000/${locale}/privacynotincluded`;
  },
};
