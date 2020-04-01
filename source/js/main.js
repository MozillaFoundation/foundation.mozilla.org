/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from "react";
import ReactDOM from "react-dom";
import * as Sentry from "@sentry/browser";
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

import { bindEventHandlers as bindMozFestEventHandlers } from "./mozfest";

import primaryNav from "./primary-nav.js";
import youTubeRegretsTunnel from "./youtube-regrets.js";

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

    this.fetchEnv(envData => {
      env = envData;
      networkSiteURL = env.NETWORK_SITE_URL;

      if (env.SENTRY_DSN) {
        // Initialize Sentry error reporting
        Sentry.init({
          dsn: env.SENTRY_DSN,
          release: env.RELEASE_VERSION,
          environment: env.SENTRY_ENVIRONMENT
        });
      }

      csrfToken = document.querySelector(`meta[name="csrf-token"]`);
      csrfToken = csrfToken ? csrfToken.getAttribute(`content`) : false;

      // HEROKU_APP_DOMAIN is used by review apps
      if (!networkSiteURL && env.HEROKU_APP_NAME) {
        networkSiteURL = `https://${env.HEROKU_APP_NAME}.herokuapp.com`;
      }

      this.injectReactComponents();
      this.bindHandlers();

      // bind MozFest specific script if on MozFest pages
      if (document.querySelector("body").classList.contains("mozfest")) {
        bindMozFestEventHandlers();
      }

      // initialize YouTube Regret interactive tunnel if on YouTube Regrets page
      if (document.querySelector("#view-youtube-regrets")) {
        youTubeRegretsTunnel.init();
      }

      // Record that we're done, when we're really done.
      Promise.all(apps).then(() => {
        window[`main-js:react:finished`] = true;
      });
    });
  },

  fetchEnv(callback) {
    let envReq = new XMLHttpRequest();

    envReq.addEventListener(`load`, () => {
      callback.call(this, JSON.parse(envReq.response));
    });

    envReq.open(`GET`, `/environment.json`);
    envReq.send();
  },

  bindHandlers() {
    bindCommonEventHandlers();
    bindWindowEventHandlers();
    bindEventHandlers();

    initializePrimaryNav(networkSiteURL, csrfToken, primaryNav);
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents() {
    injectCommonReactComponents(apps, networkSiteURL, csrfToken);
    injectReactComponents(apps, networkSiteURL, env);
  }
};

main.init();
