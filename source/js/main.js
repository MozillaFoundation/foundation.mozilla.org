/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactDOM from 'react-dom';

import JoinUs from './components/join.jsx';

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
