import DNT from "../dnt.js";
import ReactGA from "../react-ga-proxy.js";

/**
 * initialize Google Analytics and tracking pageviews
 */
const init = () => {
  const gaMeta = document.querySelector(`meta[name="ga-identifier"]`);

  if (!gaMeta) return;

  let gaIdentifier = gaMeta.getAttribute(`content`);

  if (!gaIdentifier) {
    console.warn(`No GA identifier found: skipping bootstrap step`);
  }

  if (DNT.allowTracking) {
    ReactGA.initialize(gaIdentifier);
    ReactGA.pageview(window.location.pathname);
  }
};

export default {
  init: init
};
