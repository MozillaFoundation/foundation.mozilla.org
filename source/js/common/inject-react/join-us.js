import React from "react";
import { createRoot } from "react-dom/client";
import JoinUs from "../../components/join/join.jsx";

/**
 * Inject newsletter signup forms
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 * @param {String} siteUrl Foundation site base URL
 */
export default (apps, siteUrl) => {
  // excluding `.join-us.on-nav` because it's taken care of by nav-newsletter.js
  document
    .querySelectorAll(`.join-us:not(.on-nav):not(.react-rendered)`)
    .forEach((element) => {
      const props = element.dataset;
      const sid = props.signupId || 0;

      props.apiUrl = `${siteUrl}/api/campaign/signups/${sid}/`;
      props.isHidden = false;

      apps.push(
        new Promise((resolve) => {
          const root = createRoot(element);
          root.render(<JoinUs {...props} whenLoaded={() => resolve()} />);
        })
      );
    });
};
