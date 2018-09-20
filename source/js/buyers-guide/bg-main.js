import React from 'react';
import ReactDOM from 'react-dom';

import Creepometer from './components/creepometer/creepometer.jsx';
import Criterion from './components/criterion/criterion.jsx';

let main = {
  init() {
    this.injectReactComponents();
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents() {
    if (document.querySelectorAll(`.creepometer`)) {
      Array.from(document.querySelectorAll(`.creepometer`)).forEach(element => {
        ReactDOM.render(<Creepometer/>, element);
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
