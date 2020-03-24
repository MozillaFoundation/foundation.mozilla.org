import ReactGA from "react-ga";
import { googleAnalytics } from "../common";

// A no-operation object with the same API surface
// as ReactGA, for when tracking is not appreciated:
const noop = {
  initialize: () => {},
  pageview: () => {},
  event: () => {}
};

const TrackingObject = googleAnalytics.doNotTrack ? noop : ReactGA;

export default TrackingObject;
