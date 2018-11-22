import React from 'react';
import ReactDOM from 'react-dom';
import ReactGA from './react-ga-proxy.js';

import primaryNav from './components/primary-nav/primary-nav.js';
import CreepVote from './components/creep-vote/creep-vote.jsx';
import Creepometer from './components/creepometer/creepometer.jsx';
import DonateModal from './components/donate-modal/donate-modal.jsx';
import Filter from './components/filter/filter.jsx';

import HomepageSlider from './homepage-c-slider.js';
import ProductGA from './product-analytics.js';

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
        ReactDOM.render(<Filter />, filter);
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

          let textArea = document.createElement(`textarea`);

          textArea.setAttribute(`contenteditable`, true);
          textArea.setAttribute(`readonly`, false);

          //
          // *** This styling is an extra step which is likely not required. ***
          //
          // Why is it here? To ensure:
          // 1. the element is able to have focus and selection.
          // 2. if element was to flash render it has minimal visual impact.
          // 3. less flakyness with selection and copying which **might** occur if
          //    the textarea element is not visible.
          //
          // The likelihood is the element won't even render, not even a flash,
          // so some of these are just precautions. However in IE the element
          // is visible whilst the popup box asking the user for permission for
          // the web page to copy to the clipboard.
          //

          // Place in top-left corner of screen regardless of scroll position.
          textArea.style.position = `fixed`;
          textArea.style.top = 0;
          textArea.style.left = 0;

          // Ensure it has a small width and height. Setting to 1px / 1em
          // doesn't work as this gives a negative w/h on some browsers.
          textArea.style.width = `2em`;
          textArea.style.height = `2em`;

          // We don't need padding, reducing the size if it does flash render.
          textArea.style.padding = 0;

          // Clean up any borders.
          textArea.style.border = `none`;
          textArea.style.outline = `none`;
          textArea.style.boxShadow = `none`;

          // Avoid flash of white box if rendered for any reason.
          textArea.style.background = `transparent`;

          textArea.value = window.location.href;
          document.body.appendChild(textArea);

          // Simply running textArea.select() and document.execCommand(`copy`) won't work on iOS Safari
          // Below is the suggested solution to make copying and pasting working more cross-platform
          // For details see https://stackoverflow.com/a/34046084
          let range = document.createRange();
          let selection = window.getSelection();

          range.selectNodeContents(textArea);

          selection.removeAllRanges();
          selection.addRange(range);

          textArea.setSelectionRange(0, textArea.value.length);

          try {
            document.execCommand(`copy`);

            let target = event.target;

            if (target.dataset && target.dataset.successText) {
              let defaultText = target.innerText;

              target.innerText = target.dataset.successText;
              target.classList.add(`copied`);

              setTimeout(() => {
                target.innerText = defaultText;
                target.classList.remove(`copied`);
              }, 3000);
            }
          } catch (err) {
            console.error(`Copy failed.`);
          }

          document.body.removeChild(textArea);
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

        ReactDOM.render(<CreepVote csrf={csrf.value} productName={productName} productID={parseInt(productID,10)} votes={votes}/>, element);
      });
    }

    let creepometerTargets = document.querySelectorAll(`.creepometer-target`);

    if (creepometerTargets.length > 0) {
      Array.from(creepometerTargets).forEach(element => {
        let initialValue = element.dataset.initialValue;

        ReactDOM.render(<Creepometer initialValue={initialValue} />, element);
      });
    }

    let donationModal = document.querySelector(`.donate-modal-wrapper`);

    if (donationModal) {
      ReactDOM.render(<DonateModal />, donationModal);
    }

  }
};

main.init();
