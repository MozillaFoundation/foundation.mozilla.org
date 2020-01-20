import React from "react";
import ReactDOM from "react-dom";
import JoinUs from "../../components/join/join.jsx";
import { LocalizationProvider } from "@fluent/react";
import { getBundles } from "../../l10n";

/**
 * Inject newsletter signup forms
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 * @param {String} siteUrl Foundation site base URL
 * @param {String} csrfToken CSRF Token
 */
export default (apps, siteUrl, csrfToken) => {
  // excluding `.join-us.on-nav` because it's taken care of by nav-newsletter.js
  document.querySelectorAll(`.join-us:not(.on-nav)`).forEach((element) => {
    const props = element.dataset;
    const sid = props.signupId || 0;

    props.apiUrl = `${siteUrl}/api/campaign/signups/${sid}/`;
    props.csrfToken = props.csrfToken || csrfToken;
    props.isHidden = false;

    apps.push(
      new Promise((resolve) => {
        ReactDOM.render(
          <LocalizationProvider l10n={getBundles()}>
            <JoinUs {...props} whenLoaded={() => resolve()} />
          </LocalizationProvider>,
          element
        );
      })
    );
  });
};
