import { createRoot } from "react-dom/client";
import PulseProjectList from "../../components/pulse-project-list/pulse-project-list.jsx";

/**
 * Inject Pulse project list
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 * @param {Object} env Object of environment variables
 */
export default (apps, env) => {
  document.querySelectorAll(`.pulse-project-list`).forEach((target) => {
    apps.push(
      new Promise((resolve) => {
        const root = createRoot(target);
        root.render(
          <PulseProjectList
            env={env}
            featured={target.dataset.featured === `True`}
            help={target.dataset.help}
            issues={target.dataset.issues}
            max={parseInt(target.dataset.max, 10)}
            query={target.dataset.query || ``}
            reverseChronological={target.dataset.reversed === `True`}
            whenLoaded={() => resolve()}
          />
        );
      })
    );
  });
};
