import ReactDOM from "react-dom";
import Storage from "../storage.js";
import {
  bindCommonEventHandlers,
  GoogleAnalytics,
  initializePrimaryNav,
  injectCommonReactComponents,
} from "../common";

import { injectReactComponents, bindEventHandlers } from "./index";
import injectMultipageNav from "../foundation/inject-react/multipage-nav.js";

import primaryNav from "../primary-nav.js";

import HomepageSlider from "./homepage-c-slider.js";
import AnalyticsEvents from "./analytics-events.js";
import initializeSentry from "../common/sentry-config.js";
import PNIMobileNav from "./pni-mobile-nav.js";

// Initializing component a11y browser console logging
if (
  typeof process !== "undefined" &&
  process.env &&
  process.env.NODE_ENV === "development"
) {
  axe = require("react-axe");
  axe(React, ReactDOM, 1000);
}

// Track all ReactDOM.render calls so we can use a Promise.all()
// all the way at the end to make sure we don't report "we are done"
// until all the React stuff is _actually_ done.
const apps = [];

let env, networkSiteURL;

let main = {
  init() {
    GoogleAnalytics.init();

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

      // Checking newsletter subscription status
      const sessionStorage = Storage.sessionStorage;

      let queryString = new URLSearchParams(window.location.search);
      let subscribedValue = queryString.get("subscribed");

      if (subscribedValue) {
        let subscribed = subscribedValue === "1";
        sessionStorage.setItem("subscribed", subscribed);
      }

      // HEROKU_APP_DOMAIN is used by review apps
      if (!networkSiteURL && env.HEROKU_APP_NAME) {
        networkSiteURL = `https://${env.HEROKU_APP_NAME}.herokuapp.com`;
      }

      PNIMobileNav.init();
      this.injectReactComponents();
      this.bindHandlers();
      initializePrimaryNav(networkSiteURL, primaryNav);

      // Record that we're done, when we're really done.
      Promise.all(apps).then(() => {
        window[`bg-main-js:react:finished`] = true;
        this.initPageSpecificScript();
        // bind custom analytics only once everything's up and loaded
        AnalyticsEvents.init();
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
    bindEventHandlers();
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents() {
    injectCommonReactComponents(apps, networkSiteURL);
    injectReactComponents(apps, networkSiteURL);
    injectMultipageNav(apps);
  },

  initPageSpecificScript() {
    if (document.querySelector(`body.pni.catalog`)) {
      HomepageSlider.init();
    }
  },
};

main.init();
