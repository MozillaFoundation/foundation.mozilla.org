import React from "react";
import ReactDOM from "react-dom";
import ReactGA from "../react-ga-proxy.js";

import primaryNav from "./components/primary-nav/primary-nav.js";
import navNewsletter from "../nav-newsletter.js";
import CreepVote from "./components/creep-vote/creep-vote.jsx";
import Creepometer from "./components/creepometer/creepometer.jsx";
import Filter from "./components/filter/filter.jsx";
import JoinUs from "../components/join/join.jsx";

import copyToClipboard from "../../js/copy-to-clipboard.js";
import HomepageSlider from "./homepage-c-slider.js";
import ProductGA from "./product-analytics.js";

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

      csrfToken = document.querySelector('meta[name="csrf-token"]');
      csrfToken = csrfToken ? csrfToken.getAttribute("content") : false;

      // HEROKU_APP_DOMAIN is used by review apps
      if (!networkSiteURL && env.HEROKU_APP_NAME) {
        networkSiteURL = `https://${env.HEROKU_APP_NAME}.herokuapp.com`;
      }

      // TODO: this should probably tap into the analytics.js file that
      // we use in main.js so that we only have one place where top level
      // changes to how analytics works need to be made.

      const gaMeta = document.querySelector(`meta[name="ga-identifier"]`);
      if (gaMeta) {
        let gaIdentifier = gaMeta.getAttribute(`content`);
        ReactGA.initialize(gaIdentifier); // UA-87658599-6 by default
        ReactGA.pageview(window.location.pathname);
      } else {
        console.warn(`No GA identifier found: skipping bootstrap step`);
      }

      this.enableCopyLinks();
      this.injectReactComponents();

      primaryNav.init();
      navNewsletter.init(networkSiteURL, csrfToken);

      if (document.getElementById(`view-home`)) {
        HomepageSlider.init();

        let filter = document.querySelector(`#product-filter`);

        if (filter) {
          apps.push(
            new Promise(resolve => {
              ReactDOM.render(<Filter whenLoaded={() => resolve()} />, filter);
            })
          );
        }
      }

      // Record that we're done, when we're really done.
      Promise.all(apps).then(() => {
        window[`bg-main-js:react:finished`] = true;
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

  enableCopyLinks() {
    if (document.querySelectorAll(`.copy-link`)) {
      Array.from(document.querySelectorAll(`.copy-link`)).forEach(element => {
        element.addEventListener(`click`, event => {
          event.preventDefault();

          let productBox = document.querySelector(
            `.product-detail .h1-heading`
          );
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
    }
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents() {
    let creepVoteTargets = document.querySelectorAll(`.creep-vote-target`);

    if (creepVoteTargets.length > 0) {
      Array.from(creepVoteTargets).forEach(element => {
        let csrf = element.querySelector(`input[name=csrfmiddlewaretoken]`);
        let productName = element.dataset.productName;
        let productID = element.querySelector(`input[name=productID]`).value;
        let votes = element.querySelector(`input[name=votes]`).value;

        try {
          votes = JSON.parse(votes.replace(/'/g, `"`));
        } catch (e) {
          votes = {
            creepiness: {
              average: 50,
              vote_breakdown: { "0": 0, "1": 0, "2": 0, "3": 0, "4": 0 }
            },
            confidence: { "0": 0, "1": 0 }
          };
        }

        apps.push(
          new Promise(resolve => {
            ReactDOM.render(
              <CreepVote
                csrf={csrf.value}
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
    }

    let creepometerTargets = document.querySelectorAll(`.creepometer-target`);

    if (creepometerTargets.length > 0) {
      Array.from(creepometerTargets).forEach(element => {
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

    if (document.querySelectorAll(`.join-us`)) {
      var elements = Array.from(document.querySelectorAll(`.join-us`));

      if (elements.length) {
        elements.forEach(element => {
          var props = element.dataset;

          props.apiUrl = `${networkSiteURL}/api/campaign/signups/${props.signupId ||
            0}/`;

          props.csrfToken = props.csrfToken || csrfToken;
          props.isHidden = false;

          apps.push(
            new Promise(resolve => {
              ReactDOM.render(
                <JoinUs {...props} whenLoaded={() => resolve()} />,
                element
              );
            })
          );
        });
      }
    }
  }
};

main.init();
