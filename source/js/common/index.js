/**
 * The following modules are the common modules which need to be called
 * on all pages on the main Foundation site, apps, and microsites.
 * e.g., Foundation site, PNI, MozFest etc
 */
export { bindEventHandlers } from "./template-js-handles";
export { googleAnalytics } from "./google-analytics";
export { initializePrimaryNav } from "./initialize-primary-nav";
export { injectReactComponents } from "./inject-react";
