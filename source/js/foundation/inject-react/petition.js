import React from "react";
import ReactDOM from "react-dom";
import { LocalizationProvider } from "@fluent/react";
import { getBundles } from "../../l10n";
import Petition from "../../components/petition/petition.jsx";

/**
 * Inject petition forms
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 * @param {String} siteUrl Foundation site base URL
 */
export default (apps, siteUrl) => {
  // petition elements
  var subscribed = false;

  if (window.location.search.indexOf(`subscribed=1`) !== -1) {
    subscribed = true;
  }

  document.querySelectorAll(`.sign-petition`).forEach((element) => {
    var props = element.dataset;

    props.apiUrl = `${siteUrl}/api/campaign/petitions/${props.petitionId}/`;

    apps.push(
      new Promise((resolve) => {
        ReactDOM.render(
          <LocalizationProvider l10n={getBundles()}>
            <Petition
              {...props}
              isHidden={false}
              subscribed={subscribed}
              whenLoaded={() => resolve()}
            />
          </LocalizationProvider>,
          element
        );
      })
    );
  });
};
