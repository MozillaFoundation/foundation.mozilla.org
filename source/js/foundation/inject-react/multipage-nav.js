import React from "react";
import ReactDOM from "react-dom";
import MultipageNavMobile from "../../components/multipage-nav-mobile/multipage-nav-mobile.jsx";

/**
 * Inject multipage navs (secondary navs)
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 */
export default apps => {
  let links = document.querySelectorAll(`#multipage-nav a`).map(link => {
    return {
      label: link.textContent.trim(),
      href: link.getAttribute(`href`),
      isActive: !!link.getAttribute(`class`).match(/active/)
    };
  });

  apps.push(
    new Promise(resolve => {
      ReactDOM.render(
        <MultipageNavMobile links={links} whenLoaded={() => resolve()} />,
        document.querySelector(`#multipage-nav-mobile .container .row .col-12`)
      );
    })
  );
};
