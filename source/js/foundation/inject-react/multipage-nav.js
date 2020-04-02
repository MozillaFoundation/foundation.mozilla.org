import React from "react";
import ReactDOM from "react-dom";
import MultipageNavMobile from "../../components/multipage-nav-mobile/multipage-nav-mobile.jsx";

/**
 * Inject multipage navs (secondary navs)
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 */
export default apps => {
  if (document.querySelector(`#multipage-nav`)) {
    let links = [];

    links = [].map.call(
      document.querySelectorAll(`#multipage-nav a`),
      child => {
        return {
          label: child.textContent.trim(),
          href: child.getAttribute(`href`),
          isActive: !!child.getAttribute(`class`).match(/active/)
        };
      }
    );

    apps.push(
      new Promise(resolve => {
        ReactDOM.render(
          <MultipageNavMobile links={links} whenLoaded={() => resolve()} />,
          document.querySelector(
            `#multipage-nav-mobile .container .row .col-12`
          )
        );
      })
    );
  }
};
