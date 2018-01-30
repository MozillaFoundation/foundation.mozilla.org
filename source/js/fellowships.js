/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactDOM from 'react-dom';

import Person from './components/people/person.jsx';

// Embed various Fellowships pages related React components
function injectReactComponents() {
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
      affiliations: [`Stanford University Professor; YouthLAB founder`],
      'fellow_directory_link': { type: `science`, link: `/fellowships/directory` }
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
      affiliations: [`Stanford University Professor; YouthLAB founder`],
      'fellow_directory_link': { type: `science`, link: `/fellowships/directory` }
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
      affiliations: [ `Stanford University Professor; YouthLAB founder`],
      'fellow_directory_link': { type: `science`, link: `/fellowships/directory` }
    };

    ReactDOM.render(<Person metadata={metadata} />, document.getElementById(`featured-fellow-support-page`));
  }
}

export default { injectReactComponents };
