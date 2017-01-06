/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactDOM from 'react-dom';

if (document.getElementById(`footer`)) {
  ReactDOM.render(
    <h6>Footer (via React)</h6>,
    document.getElementById(`footer`)
  );
}
