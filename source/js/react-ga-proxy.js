import DNT from './dnt.js';
import ReactGA from 'react-ga';

// A no-operation object with the same API surface
// as ReactGA, for when tracking is not appreciated:
const noop = {
  initialize: () => {},
  pageview: () => {},
  event: () => {}
};

const TrackingObject = DNT.allowTracking ? ReactGA : noop;

export default TrackingObject;
