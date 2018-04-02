/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactDOM from 'react-dom';

import Person from './components/people/person.jsx';
import LoadingIndicator from './components/loading-indicator/loading-indicator.jsx';

const CURRENT_YEAR = new Date().getFullYear();

// Currently just showing fellows for current year,
//  but can be modified to an array of years (Numbers and/or Strings)
const DIRECTORY_PROGRAM_YEARS = [CURRENT_YEAR, CURRENT_YEAR + 1];

let pulseApiDomain = ``;
let pulseDomain = ``;

// NOTE: sort on client side for now since API doesn't have the ability
// to return alphabetically sorted list
const sortByName = (a, b) =>
  a.name.toLowerCase() < b.name.toLowerCase() ? -1 : 1;

function getFellows(params, callback) {
  Object.assign(params, {'profile_type': `fellow`});

  let queryString = Object.entries(params).map(pair => pair.map(encodeURIComponent).join(`=`)).join(`&`);
  let req = new XMLHttpRequest();

  req.addEventListener(`load`, () => callback(JSON.parse(req.response)));

  req.open(`GET`, `https://${pulseApiDomain}/api/pulse/v2/profiles/?${queryString}`);
  req.send();
}

function renderFellowCard(fellow) {
  // massage fellow's Pulse profile data and pass it to <Person> to render

  let links = {};
  let programType = fellow.program_type && fellow.program_type.toLowerCase() === `in residence` ? `Fellow in Residence` : fellow.program_type;
  let issues = fellow.issues;

  issues.unshift(programType);

  if ( fellow.twitter ) {
    links.twitter = fellow.twitter;
  }

  if ( fellow.linkedin ) {
    links.linkedIn = fellow.linkedin;
  }

  let metadata = {
    'internet_health_issues': issues,
    links: links,
    name: fellow.name,
    role: `${fellow.profile_type}, ${fellow.program_year}`,
    image: fellow.thumbnail,
    location: fellow.location,
    affiliations: [], // don't show affiliations meta for now
    'custom_link': { text: `See work`, link: `https://${pulseDomain}/profile/${fellow.profile_id}` }
  };

  return <Person metadata={metadata} key={fellow.name} />;
}

function groupFellowsByAttr(attribute, fellows) {
  if (!attribute) {
    return false;
  }

  let fellowsGroup = {};

  fellows.forEach(fellow => {
    let attr = fellow[attribute];

    if (!attr) {
      return;
    }

    attr = attr.toLowerCase();

    if (!fellowsGroup[attr]) {
      fellowsGroup[attr] = [fellow];
    } else {
      fellowsGroup[attr].push(fellow);
    }
  });

  return fellowsGroup;
}

function renderFellowsOnDirectoryPage() {
  const CONTAINER = document.getElementById(`fellows-directory-current`);

  // show loading indicator
  ReactDOM.render(<div className="mx-auto my-5 text-center"><LoadingIndicator /></div>, CONTAINER);

  // get fellow info from Pulse
  getFellows({}, fellows => {
    fellows = fellows.filter(fellow => {
      // NOTE: we don't have that many fellows yet
      // so it's faster to do client side filtering than making multiple API calls
      // just to get fellows from years specified in DIRECTORY_PROGRAM_YEARS
      let matched = false;

      for (let i = 0; i < DIRECTORY_PROGRAM_YEARS.length; i++) {
        if (fellow.program_year && fellow.program_year === DIRECTORY_PROGRAM_YEARS[i].toString()) {
          matched = true;
          break;
        }
      }

      return matched;
    }).sort(sortByName);

    let section = <div className="row my-4" id={`fellowships-directory-`}>
      <div className="col-12">
        <div className="row">
          {fellows.map(renderFellowCard)}
        </div>
      </div>
      <div className="col-12 text-center mt-3 mb-5">
        <a href="/fellowships/directory/archive" className="btn btn-ghost">See Fellows from Previous Years</a>
      </div>
    </div>;

    ReactDOM.render(<div className="featured-fellow">{section}</div>, CONTAINER);
  });
}

function renderFellowsOnDirectoryByTypePage() {
  const CONTAINER = document.getElementById(`fellows-directory-archive`);

  // show loading indicator
  ReactDOM.render(<div className="mx-auto my-5 text-center"><LoadingIndicator /></div>, CONTAINER);

  // get fellow info from Pulse
  getFellows({}, fellows => {
    let fellowsByYear = groupFellowsByAttr(`program_year`, fellows);

    let sections = Object.keys(fellowsByYear).filter((year) => parseInt(year, 10) < CURRENT_YEAR).sort().reverse().map(year => {
      return <div className="row mb-5" key={year}>
        <div className="col-12">
          <div className="mb-4">
            <h2 className="h2-typeaccents-gray">{year}</h2>
          </div>
        </div>
        {fellowsByYear[year].sort(sortByName).map(renderFellowCard)}
      </div>;
    });

    ReactDOM.render(<div className="featured-fellow">{sections}</div>, CONTAINER);
  });
}

// Embed various Fellowships pages related React components
function injectReactComponents(env) {
  pulseApiDomain = env.PULSE_API_DOMAIN;
  pulseDomain = env.PULSE_DOMAIN;

  // Fellows on Fellows Directory page
  if (document.getElementById(`fellows-directory-current`)) {
    renderFellowsOnDirectoryPage();
  }

  // Fellows on individual Directory page (e.g., science directory, open web directory)
  if (document.getElementById(`fellows-directory-archive`)) {
    renderFellowsOnDirectoryByTypePage();
  }
}

export default { injectReactComponents };
