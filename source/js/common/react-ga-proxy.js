import ReactGA from "react-ga";
import { GoogleAnalytics } from "./google-analytics.js";

// A no-operation object with the same API surface
// as ReactGA, for when tracking is not appreciated:
const noop = {
  initialize: () => {},
  pageview: () => {},
  event: () => {},
};

const TrackingObject = GoogleAnalytics.doNotTrack ? noop : ReactGA;

export { TrackingObject as ReactGA };
