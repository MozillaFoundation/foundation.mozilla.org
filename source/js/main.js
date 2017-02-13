/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactDOM from 'react-dom';

import JoinUs from './components/join/join.jsx';
import PrimaryNav from './components/nav/nav.jsx';
import People from './components/people/people.jsx';

// Embed various React components based on the existence of containers within the current page

if (document.getElementById(`primary-nav`)) {
  let reactPrimaryNav;

  ReactDOM.render(
    <PrimaryNav ref={(primaryNav) => { reactPrimaryNav = primaryNav; }} />,
    document.getElementById(`primary-nav`)
  );

  if (document.getElementById(`burger`)) {
    document.getElementById(`burger`).addEventListener(`click`, () => {
      reactPrimaryNav.toggle();
    });
  }
}

if (document.getElementById(`join-us`)) {
  let reactJoinUs;

  ReactDOM.render(
    <JoinUs ref={(joinUs) => { reactJoinUs = joinUs; }}/>,
    document.getElementById(`join-us`)
  );

  if (document.getElementById(`join-trigger`)) {
    document.getElementById(`join-trigger`).addEventListener(`click`, () => {
      reactJoinUs.show();
    });
  }
}

// Embed additional instances of the Join Us box that don't need an API exposed (eg: Homepage)
if (document.querySelectorAll(`.join-us:not(#join-us)`)) {
  [].forEach.call(document.querySelectorAll(`.join-us:not(#join-us)`), (wrapper) => {
    ReactDOM.render(<JoinUs isHidden={false} />, wrapper);
  });
}

if (document.getElementById(`people`)) {
  ReactDOM.render(<People/>, document.getElementById(`people`));
}
