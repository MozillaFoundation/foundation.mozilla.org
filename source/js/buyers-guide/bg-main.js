import React from 'react';
import ReactDOM from 'react-dom';

import Creepometer from './components/creepometer/creepometer.jsx';

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
  }
};

main.init();
