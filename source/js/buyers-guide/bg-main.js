import React from 'react';
import ReactDOM from 'react-dom';

import primaryNav from './components/primary-nav/primary-nav.js';
import CreepVote from './components/creep-vote/creep-vote.jsx';
import Creepometer from './components/creepometer/creepometer.jsx';
import Criterion from './components/criterion/criterion.jsx';

import HomepageSlider from './homepage-c-slider.js';

let main = {
  init() {
    this.enableCopyLinks();
    this.injectReactComponents();
<<<<<<< HEAD
    primaryNav.init();
=======
    HomepageSlider.init();
>>>>>>> e2a6fa6... the start of a homepage
  },

  enableCopyLinks() {
    if (document.querySelectorAll(`.copy-link`)) {
      Array.from(document.querySelectorAll(`.copy-link`)).forEach(element => {
        element.addEventListener(`click`, (event) => {
          event.preventDefault();

          let textArea = document.createElement(`textarea`);

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
          textArea.select();

          try {
            document.execCommand(`copy`);
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
    if (document.querySelectorAll(`.creep-vote-target`)) {
      Array.from(document.querySelectorAll(`.creep-vote-target`)).forEach(element => {
        ReactDOM.render(<CreepVote />, element);
      });
    }

    if (document.querySelectorAll(`.creepometer-target`)) {
      Array.from(document.querySelectorAll(`.creepometer-target`)).forEach(element => {
        ReactDOM.render(<Creepometer initialValue={element.dataset.initialValue} />, element);
      });
    }

    if (document.querySelectorAll(`.criterion-target`)) {
      Array.from(document.querySelectorAll(`.criterion-target`)).forEach(element => {
        let meta = JSON.parse(element.dataset.meta);

        ReactDOM.render(<Criterion meta={meta}></Criterion>, element);
      });
    }
  }
};

main.init();
