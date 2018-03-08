/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactDOM from 'react-dom';

import Person from './components/people/person.jsx';
import LoadingIndicator from './components/loading-indicator/loading-indicator.jsx';

const DIRECTORY_PAGE_FILTER_OPTIONS = {'program_year': `2017`};

let pulseApiDomain = ``;
let pulseDomain = ``;

let capitalize = function(str) {
  return str.split(` `)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(` `);
}

function getFellows(params, callback) {
  Object.assign(params, {'profile_type': `fellow`});

  let queryString = Object.entries(params).map(pair => pair.map(encodeURIComponent).join(`=`)).join(`&`);
  let req = new XMLHttpRequest();

  req.addEventListener(`load`, () => callback(JSON.parse(req.response)));

  req.open(`GET`, `https://${pulseApiDomain}/api/pulse/profiles/?${queryString}`);
  req.send();
}

function renderFellowCard(fellow) {
  // massage fellow's Pulse profile data and pass it to <Person> to render

  let links = {};

  if ( fellow.twitter ) {
    links.twitter = fellow.twitter;
  }

  if ( fellow.linkedin ) {
    links.linkedIn = fellow.linkedin;
  }

  let metadata = {
    'internet_health_issues': fellow.issues,
    links: links,
    name: fellow.custom_name,
    role: `${fellow.profile_type}, ${fellow.program_type} ${fellow.program_year}`,
    image: fellow.thumbnail,
    location: fellow.location,
    affiliations: [], // don't show affiliations meta for now
    'custom_link': { text: `See work`, link: `https://${pulseDomain}/profile/${fellow.profile_id}` }
  };

  return <Person metadata={metadata} key={fellow.custom_name} />;
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

function renderFellowsOnDirectoryPage(directoryPageTypes = []) {
  const CONTAINER = document.getElementById(`fellows-directory-featured-fellows`);

  // sort them so we can show them alphabetically
  directoryPageTypes.sort();

  let getTypeSlug = function(type) {
    return type.toLowerCase().replace(`fellow`,``).trim().replace(/\s/g, `-`);
  };

  let renderFilterOption = function(option) {
    return <button
      className="btn btn-link text-capitalize"
      key={option}
      onClick={(event) => { window.scrollTo(0, document.getElementById(event.target.dataset.targetId).offsetTop); }}
      data-target-id={`fellowships-directory-${getTypeSlug(option)}`}
    >
      {option}
    </button>;
  };

  // show loading indicator
  ReactDOM.render(<div className="mx-auto my-5 text-center"><LoadingIndicator /></div>, CONTAINER);

  // get fellow info from Pulse
  getFellows(DIRECTORY_PAGE_FILTER_OPTIONS, fellows => {
    // render filter bar
    let filterBar = <div className="row">
      <div className="col-12">
        <div id="fellowships-directory-filter" className="d-flex flex-wrap p-2">
          <div className="d-inline-block mr-2"><strong>Areas:</strong></div>
          { directoryPageTypes.map(renderFilterOption) }
        </div>
      </div>
    </div>;

    // render program type sections
    let fellowsByType = groupFellowsByAttr(`program_type`, fellows);
    let sections = Object.keys(fellowsByType).sort((a, b) => {
      return directoryPageTypes.indexOf(a) - directoryPageTypes.indexOf(b);
    }).map(type => {
      // don't render any fellow profiles that we don't intend to show
      if (directoryPageTypes.indexOf(type) < 0) {
        return null;
      }

      let sectionTitle = type == `in residence` ? `Fellows in Residence` : `${capitalize(type)} Fellows`;

      return <div className="row my-4" key={type} id={`fellowships-directory-${getTypeSlug(type)}`}>
        <div className="col-12">
          <h3 className="h3-black">{sectionTitle}</h3>
          <div className="row">
            {fellowsByType[type].map(renderFellowCard)}
          </div>
        </div>
        <div className="col-12 text-center mt-3 mb-5">
          <a href={`/fellowships/directory/${getTypeSlug(type)}`} className="btn btn-ghost">See all {sectionTitle}</a>
        </div>
      </div>;
    });

    ReactDOM.render(<div>{filterBar}<div className="featured-fellow">{sections}</div></div>, CONTAINER);
  });
}

function renderFellowsOnDirectoryByTypePage() {
  const CONTAINER = document.getElementById(`fellows-directory-fellows-by-type`);

  // show loading indicator
  ReactDOM.render(<div className="mx-auto my-5 text-center"><LoadingIndicator /></div>, CONTAINER);

  // get fellow info from Pulse
  getFellows({'program_type': `${CONTAINER.dataset.type}`}, fellows => {
    let fellowsByYear = groupFellowsByAttr(`program_year`, fellows);

    let sections = Object.keys(fellowsByYear).sort().reverse().map(year => {
      return <div className="row mb-5" key={year}>
        <div className="col-12">
          <div className="mb-4">
            <h2 className="h2-typeaccents-gray">{year}</h2>
          </div>
        </div>
        {fellowsByYear[year].map(renderFellowCard)}
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
  if (document.getElementById(`fellows-directory-featured-fellows`)) {
    renderFellowsOnDirectoryPage(env.FELLOWSHIPS_DIRECTORY_TYPES.slice(0));
  }

  // Fellows on individual Directory page (e.g., science directory, open web directory)
  if (document.getElementById(`fellows-directory-fellows-by-type`)) {
    renderFellowsOnDirectoryByTypePage();
  }
}

export default { injectReactComponents };
