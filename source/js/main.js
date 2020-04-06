/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from "react";
import ReactDOM from "react-dom";
import {
  bindCommonEventHandlers,
  GoogleAnalytics,
  initializePrimaryNav,
  injectCommonReactComponents,
  ReactGA
} from "./common";

import { bindEventHandlers, injectReactComponents } from "./foundation";

import primaryNav from "./primary-nav.js";
import bindMozFestGA from "./mozfest-ga.js";
import bindMozFestEventHandlers from "./mozfest-event-handlers.js";
import youTubeRegretsTunnel from "./youtube-regrets.js";
import initializeSentry from "./common/sentry-config.js";

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

      GoogleAnalytics.init();

      this.injectReactComponents();
      this.bindGlobalHandlers();
      this.bindGAEventTrackers();

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

  fetchHomeDataIfNeeded(callback) {
    // Only fetch data if you're on the homepage
    if (document.querySelector(`#view-home`)) {
      let homepageReq = new XMLHttpRequest();

      homepageReq.addEventListener(`load`, () => {
        callback.call(this, JSON.parse(homepageReq.response));
      });

      homepageReq.open(`GET`, `${networkSiteURL}/api/homepage/`);
      homepageReq.send();
    } else {
      callback.call(this, {});
    }
  },

  bindGlobalHandlers() {
    // Track window scroll position and add/remove class to change sticky header appearance

    let lastKnownScrollPosition = 0;
    let ticking = false;
    let elBurgerWrapper = document.querySelector(`.wrapper-burger`);

    let adjustNavbar = scrollPosition => {
      if (scrollPosition > 0) {
        elBurgerWrapper.classList.add(`scrolled`);
      } else {
        elBurgerWrapper.classList.remove(`scrolled`);
      }
    };

    let elCtaAnchor = document.querySelector(`#cta-anchor`);
    let elStickyButton = document.querySelector(
      `.narrow-sticky-button-container`
    );
    let noopCtaButton = () => {};
    let adjustCtaButton = noopCtaButton;

    if (elCtaAnchor && elStickyButton) {
      let getAnchorPosition = () => {
        return (
          elCtaAnchor.getBoundingClientRect().top +
          window.scrollY -
          window.innerHeight
        );
      };

      let ctaAnchorPosition = getAnchorPosition();

      window.addEventListener(`resize`, () => {
        ctaAnchorPosition = getAnchorPosition();
      });

      let scrollCtaButton = scrollPosition => {
        if (scrollPosition > ctaAnchorPosition) {
          elStickyButton.classList.add(`hidden`);
          adjustCtaButton = noopCtaButton;
        }
      };

      let initCtaButton = scrollPosition => {
        if (scrollPosition <= ctaAnchorPosition) {
          elStickyButton.classList.remove(`hidden`);
          adjustCtaButton = scrollCtaButton;
        }
      };

      adjustCtaButton = initCtaButton;
    }

    let onScroll = () => {
      lastKnownScrollPosition = window.scrollY;

      if (!ticking) {
        window.requestAnimationFrame(() => {
          adjustNavbar(lastKnownScrollPosition);
          adjustCtaButton(lastKnownScrollPosition);
          ticking = false;
        });
      }

      ticking = true;
    };

    window.addEventListener(`scroll`, onScroll);

    // Toggle sticky share buttons on blog page

    let blogPageStickyButtons = document.querySelector(
      `#view-blog .blog-sticky-side .share-button-group`
    );
    let blogPageFullButtons = document.querySelector(
      `#view-blog .blog-body .share-button-group`
    );

    if (blogPageStickyButtons && blogPageFullButtons) {
      const isInViewport = element => {
        let box = element.getBoundingClientRect();

        return box.top <= window.innerHeight && box.top + box.height >= 0;
      };

      const toggleStickyButtons = () => {
        if (isInViewport(blogPageFullButtons)) {
          blogPageStickyButtons.classList.add(`faded`);
        } else {
          blogPageStickyButtons.classList.remove(`faded`);
        }
      };

      window.addEventListener(`scroll`, toggleStickyButtons);
      toggleStickyButtons();
    }

    // Call once to get scroll position on initial page load.
    onScroll();

    initializePrimaryNav(networkSiteURL, csrfToken, primaryNav);
    youTubeRegretsTunnel.init();

    // Extra tracking

    let donateHeaderBtn = document.getElementById(`donate-header-btn`);
    if (donateHeaderBtn) {
      donateHeaderBtn.addEventListener(`click`, () => {
        ReactGA.event({
          category: `donate`,
          action: `donate button tap`,
          label: `${document.title} header`
        });
      });
    }

    bindCommonEventHandlers();
  },

  bindGAEventTrackers() {
    // MozFest specific scripts
    bindMozFestGA();
    bindMozFestEventHandlers();
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents() {
    injectCommonReactComponents(apps, networkSiteURL, csrfToken);
    injectReactComponents(apps, networkSiteURL, env);

    bindEventHandlers();
  }
};

main.init();
