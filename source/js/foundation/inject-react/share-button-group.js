import React from "react";
import ReactDOM from "react-dom";
import { LocalizationProvider } from "@fluent/react";
import { getBundles } from "../../l10n";
import ShareButtonGroup from "../../components/share-button-group/share-button-group.jsx";

/**
 * Inject share button group
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 */
export default (apps) => {
  document
    .querySelectorAll(`.share-button-group-wrapper`)
    .forEach((element) => {
      var props = element.dataset;

      apps.push(
        new Promise((resolve) => {
          ReactDOM.render(
            <LocalizationProvider l10n={getBundles()}>
              <ShareButtonGroup {...props} whenLoaded={() => resolve()} />
            </LocalizationProvider>,
            element
          );
        })
      );
    });
};
