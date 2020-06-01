import { ReactGA } from "./react-ga-proxy.js";

/**
 * Check browser's "do not track" setting
 * @return {Boolean} if browser's "do not track" setting is on
 */
const checkDoNotTrack = () => {
  let _dntStatus = navigator.doNotTrack || navigator.msDoNotTrack,
    fxMatch = navigator.userAgent.match(/Firefox\/(\d+)/),
    ie10Match = navigator.userAgent.match(/MSIE 10/i),
    w8Match = navigator.appVersion.match(/Windows NT 6.2/);

  if (fxMatch && Number(fxMatch[1]) < 32) {
    _dntStatus = `Unspecified`;
  } else if (ie10Match && w8Match) {
    _dntStatus = `Unspecified`;
  } else {
    _dntStatus =
      { "0": `Disabled`, "1": `Enabled` }[_dntStatus] || `Unspecified`;
  }

  return _dntStatus === `Enabled`;
};

const DO_NOT_TRACK = checkDoNotTrack();

/**
 * Initialize Google Analytics and tracking pageviews
 */
const init = () => {
  const gaMeta = document.querySelector(`meta[name="ga-identifier"]`);

  if (!gaMeta) return;

  let gaIdentifier = gaMeta.getAttribute(`content`);

  if (!gaIdentifier) {
    console.warn(`No GA identifier found: skipping bootstrap step`);
  }

  if (!DO_NOT_TRACK) {
    ReactGA.initialize(gaIdentifier);
    ReactGA.pageview(window.location.pathname);
  }
};

/**
 * Object that includes analytics related configs and functions
 */
export const GoogleAnalytics = {
  doNotTrack: DO_NOT_TRACK,
  init: init,
};
