import React from "react";
import ReactDOM from "react-dom";
import { LocalizationProvider } from "@fluent/react";
import { getBundles } from "../../l10n";
import PulseProjectList from "../../components/pulse-project-list/pulse-project-list.jsx";

/**
 * Inject Pulse project list
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 * @param {Object} env Object of environment variables
 */
export default (apps, env) => {
  document.querySelectorAll(`.pulse-project-list`).forEach((target) => {
    apps.push(
      new Promise((resolve) => {
        ReactDOM.render(
          <LocalizationProvider l10n={getBundles()}>
            <PulseProjectList
              env={env}
              featured={target.dataset.featured === `True`}
              help={target.dataset.help}
              issues={target.dataset.issues}
              max={parseInt(target.dataset.max, 10)}
              query={target.dataset.query || ``}
              reverseChronological={target.dataset.reversed === `True`}
              whenLoaded={() => resolve()}
              directLink={target.dataset.directLink === `True`}
            />
          </LocalizationProvider>,
          target
        );
      })
    );
  });
};
