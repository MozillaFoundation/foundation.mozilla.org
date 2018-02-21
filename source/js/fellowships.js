/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactDOM from 'react-dom';

import Person from './components/people/person.jsx';

let pulseApiDomain = ``;
const DIRECOTRY_PAGE_FILTER_OPTIONS = {'program_year': `2017`};
const DIRECTORY_PAGE_TYPE_ORDER = [ `senior`, `science`, `open web`, `tech policy`, `media`];

function getFellows(params, callback) {
  Object.assign(params, {'profile_type': `fellow`});

  let queryString = Object.entries(params).map(pair => pair.map(encodeURIComponent).join(`=`)).join(`&`);
  let req = new XMLHttpRequest();

  req.addEventListener(`load`, () => {
    callback.call(this, JSON.parse(req.response));
  });

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
    role: `${fellow.program_type}${fellow.program_year ? `, ${fellow.program_year}` : ``}`,
    image: fellow.thumbnail,
    affiliations: [], // don't show affiliations meta for now
    'custom_link': { text: `See work`, link: `/fellowships/directory` }
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

    if (!fellowsGroup[attr]) {
      fellowsGroup[attr] = [fellow];
    } else {
      fellowsGroup[attr].push(fellow);
    }
  });

  return fellowsGroup;
}

function renderFellowsOnDirectoryPage() {
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
      {`${option}${option === `senior` ? ` Fellow` :``}`}
    </button>;
  };

  getFellows(DIRECOTRY_PAGE_FILTER_OPTIONS, fellows => {
    let fellowsByType = groupFellowsByAttr(`program_type`, fellows);

    // render filter bar
    let filterBar = <div className="row">
      <div className="col-12">
        <div id="fellowships-directory-filter" className="d-flex flex-wrap p-2">
          <div className="d-inline-block mr-2"><strong>Areas:</strong></div>
          { DIRECTORY_PAGE_TYPE_ORDER.map(renderFilterOption) }
        </div>
      </div>
    </div>;

    // render program type sections
    let sections = Object.keys(fellowsByType).sort((a, b) => {
      let aIndex = DIRECTORY_PAGE_TYPE_ORDER.indexOf(a.replace(`fellow`,``).trim());
      let bIndex = DIRECTORY_PAGE_TYPE_ORDER.indexOf(b.replace(`fellow`,``).trim());

      return aIndex - bIndex;
    }).map(type => {
      return <div className="row my-4" key={type} id={`fellowships-directory-${getTypeSlug(type)}`}>
        <div className="col-12">
          <h3 className="h3-black text-capitalize">{type}s</h3>
          <div className="row">
            {fellowsByType[type].map(renderFellowCard)}
          </div>
        </div>
        <div className="col-12 text-center mt-3 mb-5">
          <a href={`/fellowships/directory/${getTypeSlug(type)}`} className="btn btn-ghost">See all {type}s</a>
        </div>
      </div>;
    });

    ReactDOM.render(<div>{filterBar}<div className="featured-fellow">{sections}</div></div>, document.getElementById(`fellows-directory-featured-fellows`));
  });
}

function renderFellowsOnDirectoryByTypePage() {
  let type = document.getElementById(`fellows-directory-fellows-by-type`).dataset.type;

  getFellows({'program_type': `${type} fellow`}, fellows => {
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

    ReactDOM.render(<div className="featured-fellow">{sections}</div>, document.getElementById(`fellows-directory-fellows-by-type`));
  });
}

// Embed various Fellowships pages related React components
function injectReactComponents(pulseApiURL) {
  pulseApiDomain = pulseApiURL;

  // Science Fellowship
  if (document.getElementById(`featured-science-fellow`)) {
    let metadata = {
      featured: true,
      'internet_health_issues': [ `Decentralization`, `Open Innovation` ],
      links: [],
      name: `Firstname Surname`,
      role: `[Area Fellowship] Fellow, [Year]`,
      location: `City, Country`,
      image: `https://images.pexels.com/photos/264206/pexels-photo-264206.jpeg?w=500`,
      quote: `Quote quote quote quote quote quote quote quote quote quote quote quote.`,
      affiliations: [] // don't show affiliations meta for now
    };

    ReactDOM.render(<Person metadata={metadata} />, document.getElementById(`featured-science-fellow`));
  }

  // Open Web Fellowship
  if (document.getElementById(`featured-open-web-fellow`)) {
    let metadata = {
      featured: true,
      'internet_health_issues': [ `Decentralization`, `Open Innovation` ],
      links: [],
      name: `Firstname Surname`,
      role: `[Area Fellowship] Fellow, [Year]`,
      location: `City, Country`,
      image: `https://images.pexels.com/photos/802112/pexels-photo-802112.jpeg?w=500`,
      quote: `Quote quote quote quote quote quote quote quote quote quote quote quote.`,
      affiliations: [] // don't show affiliations meta for now
    };

    ReactDOM.render(<Person metadata={metadata} />, document.getElementById(`featured-open-web-fellow`));
  }

  // Featured fellow on Support page
  if (document.getElementById(`featured-fellow-support-page`)) {
    let metadata = {
      featured: true,
      'internet_health_issues': [ `Decentralization`, `Open Innovation` ],
      links: [],
      name: `Firstname Surname`,
      role: `[Area Fellowship] Fellow, [Year]`,
      location: `City, Country`,
      image: `https://static.pexels.com/photos/416138/pexels-photo-416138.jpeg?w=500`,
      quote: `Quote quote quote quote quote quote quote quote quote quote quote quote.`,
      affiliations: [] // don't show affiliations meta for now
    };

    ReactDOM.render(<Person metadata={metadata} />, document.getElementById(`featured-fellow-support-page`));
  }

  // Fellows on Fellows Directory page
  if (document.getElementById(`fellows-directory-featured-fellows`)) {
    renderFellowsOnDirectoryPage();
  }

  // Fellows on individual Directory page (e.g., science directory, open web directory)
  if (document.getElementById(`fellows-directory-fellows-by-type`)) {
    renderFellowsOnDirectoryByTypePage();
  }
}

export default { injectReactComponents };
