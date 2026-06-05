// Official doc from Cookie Contorl: https://cookiecontrol.com/docs/v9/
// GDPR/CCPA mode should be based on geo location
// Locale should be based on user’s browser language setting


const API_KEY = "76fd590604f568812d13d4780b846805941fe9f0";
const PRODUCT_TYPE = "CUSTOM";

CookieControl.geoTest(PRODUCT_TYPE, API_KEY, function (response) {
  console.log("geoTest response:", response);

  var config = {
    product: PRODUCT_TYPE,
    mode: response.withinEU ? "GDPR" : "CCPA",
    text: {
      title: "🍪 Cookie Test (EN)",
      intro: "English default text.",
      accept: "✅✅ Accept",
      reject: "❌❌ Reject",
    },
    locales: [
      {
        locale: "fr",
        text: {
          title: "🍪 Test de cookies (FR)",
          intro: "Texte par défaut en français.",
          acceptSettings: "✅✅ Accepter",
          rejectSettings: "❌❌ Refuser",
        },
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
