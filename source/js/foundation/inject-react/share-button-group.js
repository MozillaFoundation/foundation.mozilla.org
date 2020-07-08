import React from "react";
import ReactDOM from "react-dom";
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
            <ShareButtonGroup {...props} whenLoaded={() => resolve()} />,
            element
          );
        })
      );
    });
};
