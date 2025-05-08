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
      {
        0: `Disabled`,
        1: `Enabled`,
      }[_dntStatus] || `Unspecified`;
  }

  return _dntStatus === `Enabled`;
};

const DO_NOT_TRACK = checkDoNotTrack();

const getIdentifier = (type = "ga") => {
  const meta = document.querySelector(`meta[name="${type}-identifier"]`);

  if (!meta) return;

  let identifier = meta.getAttribute(`content`);

  if (!identifier) {
    console.warn(
      `No ${type.toUpperCase()} identifier found: skipping bootstrap step`
    );
  }

  return identifier;
};

/**
 * Initialize Google Analytics and Google Tag Manager
 */
const init = () => {
  if (!DO_NOT_TRACK) {
    const GA_ID = getIdentifier(`ga`);
    const GTM_ID = getIdentifier(`gtm`);

    if (GA_ID) {
      // Disable pageview event, but keep all the regular events for now
      // SEE: https://github.com/mozilla/foundation.mozilla.org/issues/5849
      ReactGA.initialize(GA_ID);

      // ReactGA.pageview(window.location.pathname);
    }

    if (GTM_ID) {
      (function (w, d, s, l, i) {
        w[l] = w[l] || [];
        w[l].push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
        var f = d.getElementsByTagName(s)[0],
          j = d.createElement(s),
          dl = l != "dataLayer" ? "&l=" + l : "";
        j.async = true;
        j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl;
        f.parentNode.insertBefore(j, f);
      })(window, document, "script", "dataLayer", GTM_ID);
    }
  }
};

/**
 * Object that includes analytics related configs and functions
 */
export const GoogleAnalytics = {
  doNotTrack: DO_NOT_TRACK,
  init: init,
};
