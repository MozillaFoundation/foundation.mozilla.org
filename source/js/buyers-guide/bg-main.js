import React from "react";
import ReactDOM from "react-dom";
import Storage from "../storage.js";
import {
  bindCommonEventHandlers,
  GoogleAnalytics,
  initializePrimaryNav,
  injectCommonReactComponents,
} from "../common";

import { injectReactComponents, bindEventHandlers } from "./index";
import injectMultipageNav from "../multipage-nav.js";

import primaryNav from "../primary-nav.js";

import HomepageSlider from "./template-js-handler/homepage-c-slider.js";
import NewsletterBox from "./template-js-handler/newsletter-box.js";
import AnalyticsEvents from "./analytics-events.js";
import initializeSentry from "../common/sentry-config.js";
import PNIMobileNav from "./pni-mobile-nav.js";

// Initializing component a11y browser console logging
if (process.env.NODE_ENV === "development") {
  const axe = require("@axe-core/react");
  axe(React, ReactDOM, 1000);
}

// Track all React client rendering calls so we can use a Promise.all()
// all the way at the end to make sure we don't report "we are done"
// until all the React stuff is _actually_ done.
const apps = [];

let env, networkSiteURL;

let main = {
  /**
   * Initializer
   * Injects React components and bind event handlers for PNI specific elements
   */
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

      this.injectReactComponents();
      this.bindHandlers();
      NewsletterBox.toggleVisibilityClasses();
      initializePrimaryNav(networkSiteURL, primaryNav);
      injectMultipageNav();

      // Record that we're done, when we're really done.
      Promise.all(apps).then(() => {
        document.body.classList.add(`react-loaded`);
        this.initPageSpecificScript();
        PNIMobileNav.init();
        // bind custom analytics only once everything's up and loaded
        // Analytics events does give errors quite often, do not add JS after this
        AnalyticsEvents.init();
      });
    });
  },

  /**
   * Fetch env var config from environment.json and process it for use
   * @param {Object} processEnv env var config
   */
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

  /**
   * Bind event handlers
   */
  bindHandlers() {
    bindCommonEventHandlers();
    bindEventHandlers();
  },

  /**
   * Inject React components
   */
  injectReactComponents() {
    injectCommonReactComponents(apps, networkSiteURL);
    injectReactComponents(apps, networkSiteURL);
  },

  /**
   * Initialize page specific script
   */
  initPageSpecificScript() {
    if (document.querySelector(`body.pni.catalog`)) {
      HomepageSlider.init();
    }
  },
};

main.init();
