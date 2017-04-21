/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactDOM from 'react-dom';
import Cookies from 'js-cookie';

import JoinUs from './components/join/join.jsx';
import PrimaryNav from './components/nav/nav.jsx';
import People from './components/people/people.jsx';
import PeopleBox from './components/people-box/people-box.jsx';
import Takeover from './components/takeover/takeover.jsx';

let main = {
  init () {
    this.injectReactComponents();
  },

  // Trigger blurring of page contents when primary nav is toggled
  onPrimaryNavStateChange (event) {
    let elWrapper = document.querySelector(`body > .wrapper`);

    if (event.isHidden) {
      elWrapper.classList.remove(`blurred`);
    } else {
      elWrapper.classList.add(`blurred`);
    }
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents () {
    if (document.getElementById(`primary-nav`)) {
      let reactPrimaryNav;

      ReactDOM.render(
        <PrimaryNav
          ref={(primaryNav) => { reactPrimaryNav = primaryNav; }}
          onStateChange={this.onPrimaryNavStateChange}/>,
        document.getElementById(`primary-nav`)
      );

      if (document.getElementById(`burger`)) {
        document.getElementById(`burger`).addEventListener(`click`, () => {
          reactPrimaryNav.toggle();
        });
      }
    }

    // Show Takeover for new visitors
    if (!Cookies.get(`seen-takeover`) && document.querySelector(`#view-home .takeover`)) {
      let elWrapper = document.querySelector(`#view-home > .wrapper`);

      // Don't allow the content block to scroll
      elWrapper.style.overflow = `hidden`;
      elWrapper.style.height = `100vh`;

      let onTakeoverHide = () => {
        // Allow scrolling again when the takeover is dismissed
        elWrapper.style.overflow = null;
        elWrapper.style.height = null;
      };

      ReactDOM.render(<Takeover onHide={onTakeoverHide}/>, document.querySelector(`#view-home .takeover`));
      Cookies.set(`seen-takeover`, `true`, { expires: 365 });
    }

    // Embed additional instances of the Join Us box that don't need an API exposed (eg: Homepage)
    if (document.querySelectorAll(`.join-us:not(#join-us)`)) {
      var elements = Array.from(document.querySelectorAll(`.join-us:not(#join-us)`));

      if(elements.length) {
        elements.forEach(element => {
          var props = element.dataset;

          ReactDOM.render(<JoinUs {...props} isHidden={false} />, element);
        });
      }
    }

    if (document.getElementById(`people`)) {
      ReactDOM.render(<People/>, document.getElementById(`people`));
    }

    if (document.getElementById(`people-box`)) {
      ReactDOM.render(<PeopleBox/>, document.getElementById(`people-box`));
    }

  }
};

main.init();
