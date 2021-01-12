import React from "react";
import ReactDOM from "react-dom";
import MultipageNavMobile from "../../components/multipage-nav-mobile/multipage-nav-mobile.jsx";

/**
 * Inject mobile version of multipage navs (secondary navs)
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 */
export default (apps) => {
  let targetNode = document.querySelector(
    `#multipage-nav-mobile .container .row .col-12`
  );

  if (targetNode) {
    const multipageLinks = document.querySelectorAll(`#multipage-nav a`)

    if(!multipageLinks.length) {
      // If there are no links to use from `#multipage-nav a`, hide the dropdown container and return early
      document.getElementById(`multipage-nav-mobile`).classList.add(`d-none`)
      return false
    }

    let links = Array.from(multipageLinks).map(
      (link) => {
        return {
          label: link.textContent.trim(),
          href: link.getAttribute(`href`),
          isActive: !!link.getAttribute(`class`).match(/active/),
        };
      }
    );

    apps.push(
      new Promise((resolve) => {
        ReactDOM.render(
          <MultipageNavMobile links={links} whenLoaded={() => resolve()} />,
          targetNode
        );
      })
    );
  }
};
