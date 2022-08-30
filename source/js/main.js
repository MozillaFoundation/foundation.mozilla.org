/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */
import ReactDOM from "react-dom";
import {
  bindCommonEventHandlers,
  GoogleAnalytics,
  initializePrimaryNav,
  injectCommonReactComponents,
} from "./common";

import {
  bindWindowEventHandlers,
  bindEventHandlers,
  injectReactComponents,
} from "./foundation";

import primaryNav from "./primary-nav.js";
import injectMultipageNav from "./multipage-nav.js";
import EmbedTypeform from "./embed-typeform.js";
import Dropdowns from "./dropdowns.js";
import DonateBanner from "./donate-banner";
import MozfestCarousels from "./components/carousel/carousel.js";
import FoundationCarousels from "./components/foundation-carousel/foundation-carousel.js";
import MozfestHeroCarousels from "./components/mozfest-hero-carousel/mozfest-hero-carousel";
import initializeSentry from "./common/sentry-config.js";
import YouTubeRegretsTunnel from "./foundation/pages/youtube-regrets/intro-tunnel";
import YouTubeRegretsBrowserExtension from "./foundation/pages/youtube-regrets/browser-extension";
import RegretsReporterUtmButtons from "./foundation/pages/youtube-regrets/regrets-reporter/utm-buttons";
import RegretsReporterShareButtons from "./foundation/pages/youtube-regrets/regrets-reporter/share-buttons";
import RegretsReporterTimeline from "./foundation/pages/youtube-regrets/regrets-reporter/timeline";
import { bindEventHandlers as bindRegretsReporterEventHandlers } from "./foundation/pages/youtube-regrets/regrets-reporter";
import { bindEventHandlers as bindDearInternetEventHandlers } from "./foundation/pages/dear-internet";
import { initYouTubeRegretsCategoriesBarChart } from "./foundation/pages/youtube-regrets/categories-bar-chart";
import { initYouTubeRegretsRegretRatesChart } from "./foundation/pages/youtube-regrets/regret-rates-chart";
import { initYoutubeRegretsReadMoreCategories } from "./foundation/pages/youtube-regrets/read-more-categories";
import { initYoutubeRegretsResearchCountUp } from "./foundation/pages/youtube-regrets/count-up";
import { initYoutubeRegretsAccordions } from "./foundation/pages/youtube-regrets/accordion";
import { initYouTubeRegretsRecommendationsPieChart } from "./foundation/pages/youtube-regrets/recommendations-pie-chart";
import { initYoutubeRegretsCarousel } from "./foundation/pages/youtube-regrets/carousel";
import { initYoutubeRegretsLocomotiveScroll } from "./foundation/pages/youtube-regrets/locomotive-scroll";

// Initializing component a11y browser console logging
if (
  typeof process !== "undefined" &&
  process.env &&
  process.env.NODE_ENV === "development"
) {
  axe = require("react-axe");
  axe(React, ReactDOM, 1000);
}

// To be populated via XHR and querySelector
let env, networkSiteURL;

// Track all ReactDOM.render calls so we can use a Promise.all()
// all the way at the end to make sure we don't report "we are done"
// until all the React stuff is _actually_ done.
const apps = [];

let main = {
  init() {
    injectMultipageNav();
    DonateBanner.init();
    GoogleAnalytics.init();
    EmbedTypeform.init();
    Dropdowns.init();
    FoundationCarousels.init();

    this.fetchEnv((envData) => {
      env = envData;
      networkSiteURL = env.NETWORK_SITE_URL;

      if (env.SENTRY_DSN) {
        // Initialize Sentry error reporting
        initializeSentry(
          env.SENTRY_DSN,
          env.RELEASE_VERSION,
          env.SENTRY_ENVIRONMENT
        );
      }

      // HEROKU_APP_DOMAIN is used by review apps
      if (!networkSiteURL && env.HEROKU_APP_NAME) {
        networkSiteURL = `https://${env.HEROKU_APP_NAME}.herokuapp.com`;
      }

      this.injectReactComponents();
      this.bindHandlers();
      initializePrimaryNav(networkSiteURL, primaryNav);

      // Record that we're done, when we're really done.
      Promise.all(apps).then(() => {
        document.body.classList.add(`react-loaded`);
        this.initPageSpecificScript();
      });
    });
  },

  fetchEnv(processEnv) {
    let envReq = new XMLHttpRequest();

    envReq.addEventListener(`load`, () => {
      try {
        processEnv(JSON.parse(envReq.response));
      } catch (e) {
        processEnv({});
      }
    });

    envReq.open(`GET`, `/environment.json`);
    envReq.send();
  },

  bindHandlers() {
    bindCommonEventHandlers();
    bindWindowEventHandlers();
    bindEventHandlers();
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents() {
    injectCommonReactComponents(apps, networkSiteURL);
    injectReactComponents(apps, networkSiteURL, env);
  },

  initPageSpecificScript() {
    // YouTube Regrets page
    if (document.querySelector("#view-youtube-regrets")) {
      new YouTubeRegretsTunnel();
    }

    if (document.querySelector("#view-youtube-regrets-reporter-extension")) {
      new YouTubeRegretsBrowserExtension();
    }

    // YouTube Regrets 2021 page
    if (document.querySelector("#view-youtube-regrets-2021")) {
      initYouTubeRegretsCategoriesBarChart();
      initYouTubeRegretsRegretRatesChart();
      initYoutubeRegretsReadMoreCategories();
      initYoutubeRegretsAccordions();
      initYouTubeRegretsRecommendationsPieChart();
      initYoutubeRegretsCarousel();
    }

    // Shared YouTube Regrets Pages
    if (document.querySelector(".youtube-regrets-shared")) {
      initYoutubeRegretsResearchCountUp();
    }

    if (document.querySelector("#view-youtube-regrets-2022")) {
      initYoutubeRegretsLocomotiveScroll();
    }

    // YouTube Regrets Reporter page
    if (document.querySelector("#view-youtube-regrets-reporter")) {
      new YouTubeRegretsTunnel();
      new RegretsReporterTimeline();
      bindRegretsReporterEventHandlers();
    }
    // YouTube Regrets Reporter Extension Page
    if (document.querySelector("#regrets-reporter-extension-page")) {
      new RegretsReporterUtmButtons();
      new RegretsReporterShareButtons();
    }

    // Dear Internet page
    if (document.querySelector("#view-dear-internet")) {
      bindDearInternetEventHandlers();
    }

    // Mozfest pages
    if (document.querySelector(`.mozfest`)) {
      MozfestCarousels.init();
      MozfestHeroCarousels.init();
    }
  },
};

main.init();
