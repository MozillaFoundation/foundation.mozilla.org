// Official doc from Cookie Contorl: https://cookiecontrol.com/docs/v9/
// GDPR/CCPA mode should be based on geo location
// Locale should be based on user’s browser language setting

const API_KEY = "76fd590604f568812d13d4780b846805941fe9f0";
const PRODUCT_TYPE = "CUSTOM";

CookieControl.geoTest(PRODUCT_TYPE, API_KEY, function (response) {
  console.log("geoTest response:", response);

  var config = {
    theme: "dark",
    initialState: "notify",
    product: PRODUCT_TYPE,
    mode: response.withinEU ? "GDPR" : "CCPA",
    theme: "light",
    closeStyle: "labelled",
    text: {
      title: "Help Mozilla with Analytics (EN)",
      intro:
        "We use some essential cookies to make this website. We’d like to set additional cookies to understand how you use mozillafoundation.org. Your settings improve our services.",
      acceptSettings: "Accept Analytics Cookies",
      rejectSettings: "Reject Analytics Cookies",
      closeLabel: "CLOSE",
      notifyTitle: "[Notify baner title] Help Mozilla with Analytics (EN)",
      notifyDescription:
        "[Notify baner description] We use some essential cookies to make this website. We’d like to set additional cookies to understand how you use mozillafoundation.org. Your settings improve our services.",
      accept: "Accept Analytics Cookies",
      reject: "Reject Analytics Cookies",
      settings: "Consent Settings",
    },
    optionalCookies: [
      {
        name: "analytics",
        label: "[Test] Analytical Cookies",
        description: "Description description description.",
        cookies: [],
        onAccept: function () {},
        onRevoke: function () {},
      },
      {
        name: "marketing",
        label: "[Test] Marketing Cookies",
        description: "Description description description.",
        cookies: [],
        onAccept: function () {},
        onRevoke: function () {},
      },
    ],
    locales: [
      {
        locale: "fr",
        text: {
          title: "🍪 Test de cookies (FR)",
          intro: "Texte par défaut en français.",
          acceptSettings: "✅✅ Accepter",
          rejectSettings: "❌❌ Refuser",
        },
        optionalCookies: [
          {
            name: "analytics",
            label: "[Test FR] Analytical Cookies",
            description: "Description description description.",
            cookies: [],
            onAccept: function () {},
            onRevoke: function () {},
          },
          {
            name: "marketing",
            label: "[Test FR] Marketing Cookies",
            description: "Description description description.",
            cookies: [],
            onAccept: function () {},
            onRevoke: function () {},
          },
        ],
      },
      {
        locale: "de",
        text: {
          title: "🍪 Cookie-Test (DE)",
          intro: "Standardtext auf Deutsch.",
          acceptSettings: "✅✅ Akzeptieren",
          rejectSettings: "❌❌ Ablehnen",
        },
      },
      {
        locale: "pt",
        text: {
          title: "🍪 Teste de cookies (PT)",
          intro: "Texto padrão em português.",
          acceptSettings: "✅✅ Aceitar",
          rejectSettings: "❌❌ Recusar",
        },
      },
    ],
  };

  console.log("config: ", config);

  config.apiKey = API_KEY;

  CookieControl.load(config);
});
