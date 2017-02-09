/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactDOM from 'react-dom';

import JoinUs from './components/join.jsx';
import PrimaryNav from './components/nav.jsx';

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
