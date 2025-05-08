/**
 * The following modules are the common modules which need to be called
 * on all pages on the main Foundation site, apps, and microsites.
 * e.g., Foundation site, PNI, MozFest etc
 */
export { bindCommonEventHandlers } from "./template-js-handles";
export { GoogleAnalytics } from "./google-analytics.js";
export { initializePrimaryNav } from "./initialize-primary-nav.js";
export { injectCommonReactComponents } from "./inject-react";
export { ReactGA } from "./react-ga-proxy.js";
