import React from 'react';
import ReactDOM from 'react-dom';
import ReactGA from '../react-ga-proxy.js';

import primaryNav from './components/primary-nav/primary-nav.js';
import CreepVote from './components/creep-vote/creep-vote.jsx';
import Creepometer from './components/creepometer/creepometer.jsx';
import injectDonateModal from '../donate-modal/donate-modal.jsx';
import Filter from './components/filter/filter.jsx';

import copyToClipboard from './copy-to-clipboard.js';
import HomepageSlider from './homepage-c-slider.js';
import ProductGA from './product-analytics.js';

// Track all ReactDOM.render calls so we can use a Promise.all()
// all the way at the end to make sure we don't report "we are done"
// until all the React stuff is _actually_ done.
const apps = [];

let main = {
  init() {
    ReactGA.initialize(`UA-87658599-6`);
    ReactGA.pageview(window.location.pathname);

    this.enableCopyLinks();
    this.injectReactComponents();

    primaryNav.init();

    if (document.getElementById(`pni-home`)) {
      HomepageSlider.init();

      let filter = document.querySelector(`#product-filter`);

      if (filter) {
        apps.push(new Promise(resolve => {
          ReactDOM.render(<Filter whenLoaded={() => resolve()}/>, filter);
        }));
      }
    }

    if (document.getElementById(`pni-product-page`)) {
      ProductGA.init();

      // Set up help text accordions where necessary:
      let productBox = document.querySelector(`.product-detail .h1-heading`);
      let productName = productBox ? productBox.textContent : `unknown product`;
      let criteriaWithHelp = document.querySelectorAll(`.criterion button.toggle`);

      if (criteriaWithHelp.length > 0) {
        Array.from(criteriaWithHelp).forEach(button => {
          let help = button.closest(`.criterion`).querySelector(`.helptext`);

          button.addEventListener(`click`, () => {
            button.classList.toggle(`open`);
            help.classList.toggle(`open`);

            if (help.classList.contains(`open`)) {
              ReactGA.event({
                category: `product`,
                action: `expand accordion tap`,
                label: `detail view on ${productName}`
              });
            }
          });
        });
      }
    }

    // Record that we're done, when we're really done.
    Promise.all(apps).then(() => {
      window[`bg-main-js:react:finished`] = true;
    });
  },

  enableCopyLinks() {
    if (document.querySelectorAll(`.copy-link`)) {
      Array.from(document.querySelectorAll(`.copy-link`)).forEach(element => {
        element.addEventListener(`click`, (event) => {
          event.preventDefault();

          let productBox = document.querySelector(`.product-detail .h1-heading`);
          let productTitle = productBox ? productBox.textContent : `unknown product`;

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
          votes = JSON.parse(votes.replace(/'/g,`"`));
        } catch (e) {
          votes = {
            creepiness: {
              average: 50,
              'vote_breakdown': {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0}
            },
            confidence: {'0': 0, '1': 0}
          };
        }

        apps.push(new Promise(resolve => {
          ReactDOM.render(<CreepVote csrf={csrf.value} productName={productName} productID={parseInt(productID,10)} votes={votes} whenLoaded={() => resolve()}/>, element);
        }));
      });
    }

    let creepometerTargets = document.querySelectorAll(`.creepometer-target`);

    if (creepometerTargets.length > 0) {
      Array.from(creepometerTargets).forEach(element => {
        let initialValue = element.dataset.initialValue;

        apps.push(new Promise(resolve => {
          ReactDOM.render(<Creepometer initialValue={initialValue} whenLoaded={() => resolve()}/>, element);
        }));
      });
    }

    let donationModal = document.querySelector(`.donate-modal-wrapper`);

    if (donationModal) {
      let modalOptions = {
        title: `We made this guide with support from people like you`,
        subheading: `Our supporters told us they are uncertain about how to be safer online. We listened. This guide is a result.`,
        cta: {
          title: `Help us keep this work going`,
          text: `Support Mozilla`
        },
        utm: {
          medium: `buyersguide`,
          campaign: `buyersguide2018`,
          content: `popupbutton`
        },
        ga: {
          category: `buyersguide`,
          action: `donate tap`,
          label: `donate popup on ${window.location.pathname.replace(/\w\w(-\W\W)?\/privacynotincluded\//,``)}`
        }
      };

      injectDonateModal(donationModal, modalOptions);
    }
  }
};

main.init();
