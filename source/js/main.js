/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from "react";
import ReactDOM from "react-dom";
import {
  bindCommonEventHandlers,
  GoogleAnalytics,
  initializePrimaryNav,
  injectCommonReactComponents
} from "./common";

import {
  bindWindowEventHandlers,
  bindEventHandlers,
  injectReactComponents
} from "./foundation";

import primaryNav from "./primary-nav.js";
import EmbedTF from "./embed-tf.js";
import initializeSentry from "./common/sentry-config.js";
import YouTubeRegretsTunnel from "./foundation/pages/youtube-regrets/index";

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
let env, networkSiteURL, csrfToken;

// Track all ReactDOM.render calls so we can use a Promise.all()
// all the way at the end to make sure we don't report "we are done"
// until all the React stuff is _actually_ done.
const apps = [];

let main = {
  init() {
    GoogleAnalytics.init();
    EmbedTF.init();

    this.fetchEnv(envData => {
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

      csrfToken = document.querySelector(`meta[name="csrf-token"]`);
      csrfToken = csrfToken ? csrfToken.getAttribute(`content`) : false;

      // HEROKU_APP_DOMAIN is used by review apps
      if (!networkSiteURL && env.HEROKU_APP_NAME) {
        networkSiteURL = `https://${env.HEROKU_APP_NAME}.herokuapp.com`;
      }

      this.injectReactComponents();
      this.bindHandlers();
      initializePrimaryNav(networkSiteURL, csrfToken, primaryNav);

      // Record that we're done, when we're really done.
      Promise.all(apps).then(() => {
        window[`main-js:react:finished`] = true;
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
    injectCommonReactComponents(apps, networkSiteURL, csrfToken);
    injectReactComponents(apps, networkSiteURL, env);
  },

  initPageSpecificScript() {
    // YouTube Regrets page
    if (document.querySelector("#view-youtube-regrets")) {
      new YouTubeRegretsTunnel();
    }
  }
};

main.init();
