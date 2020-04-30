import React from "react";
import ReactDOM from "react-dom";
import Storage from "../storage.js";
import {
  bindCommonEventHandlers,
  GoogleAnalytics,
  initializePrimaryNav,
  injectCommonReactComponents,
  ReactGA
} from "../common";

import primaryNav from "./components/primary-nav/primary-nav.js";
import CreepVote from "./components/creep-vote/creep-vote.jsx";
import Creepometer from "./components/creepometer/creepometer.jsx";

import copyToClipboard from "../../js/copy-to-clipboard.js";
import HomepageSlider from "./homepage-c-slider.js";
import AnalyticsEvents from "./analytics-events.js";
import initializeSentry from "../common/sentry-config.js";

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

let env, networkSiteURL, csrfToken;

let main = {
  init() {
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

      csrfToken = document.querySelector('meta[name="csrf-token"]');
      csrfToken = csrfToken ? csrfToken.getAttribute("content") : false;

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

      GoogleAnalytics.init();

      this.enableCopyLinks();
      this.injectReactComponents();

      bindCommonEventHandlers();
      initializePrimaryNav(networkSiteURL, csrfToken, primaryNav);

      if (document.getElementById(`view-home`)) {
        HomepageSlider.init();
      }

      // Record that we're done, when we're really done.
      Promise.all(apps).then(() => {
        window[`bg-main-js:react:finished`] = true;

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

  enableCopyLinks() {
    document.querySelectorAll(`.copy-link`).forEach(element => {
      element.addEventListener(`click`, event => {
        event.preventDefault();

        let productBox = document.querySelector(`.product-detail .h1-heading`);
        let productTitle = productBox
          ? productBox.textContent
          : `unknown product`;

        ReactGA.event({
          category: `product`,
          action: `copy link tap`,
          label: `copy link ${productTitle}`
        });

        copyToClipboard(event.target, window.location.href);
      });
    });
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents() {
    injectCommonReactComponents(apps, networkSiteURL, csrfToken);

    document.querySelectorAll(`.creep-vote-target`).forEach(element => {
      let csrf = element.querySelector(`input[name=csrfmiddlewaretoken]`);
      let productType = element.dataset.productType;
      let productName = element.dataset.productName;
      let productID = element.querySelector(`input[name=productID]`).value;
      let votesValue = element.querySelector(`input[name=votes]`).value;

      let votes = {
        total: 0,
        creepiness: {
          average: 50,
          vote_breakdown: { "0": 0, "1": 0, "2": 0, "3": 0, "4": 0 }
        },
        confidence: { "0": 0, "1": 0 }
      };

      if (votesValue !== "None") {
        try {
          votes = JSON.parse(votesValue.replace(/'/g, `"`));
        } catch (e) {
          // if this fails, we just use the defaults
        }
      }

      apps.push(
        new Promise(resolve => {
          ReactDOM.render(
            <CreepVote
              csrf={csrf.value}
              productType={productType}
              productName={productName}
              productID={parseInt(productID, 10)}
              votes={votes}
              whenLoaded={() => resolve()}
              joinUsCSRF={csrfToken}
              joinUsApiUrl={`${networkSiteURL}/api/campaign/signups/0/`}
            />,
            element
          );
        })
      );
    });

    document.querySelectorAll(`.creepometer-target`).forEach(element => {
      let initialValue = element.dataset.initialValue;
      apps.push(
        new Promise(resolve => {
          ReactDOM.render(
            <Creepometer
              initialValue={initialValue}
              whenLoaded={() => resolve()}
            />,
            element
          );
        })
      );
    });
  }
};

main.init();
