import React from 'react';
import PropTypes from 'prop-types';
import Person from '../../components/people/person.jsx';
import LoadingIndicator from '../../components/loading-indicator/loading-indicator.jsx';

export default class FellowList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      fellows: null
    };
  }

  fetchFellows(query) {
    Object.assign(query, {
      'profile_type': `fellow`,
      'ordering': `custom_name`
    });

    let queryString = Object.entries(query).map(pair => pair.map(encodeURIComponent).join(`=`)).join(`&`);
    let xhr = new XMLHttpRequest();

    xhr.addEventListener(`load`, () => {
      this.setState({
        fellows: JSON.parse(xhr.response)
      });
    });

    xhr.open(`GET`, `${this.props.env.PULSE_API_DOMAIN}/api/pulse/v2/profiles/?${queryString}`);
    xhr.send();
  }

  componentDidMount() {
    this.fetchFellows(this.props.query);
  }

  componentDidUpdate(prevProps) {
    // new props were received. let's check if it's necessary to fetch data again
    if (this.hasQueryChanged(prevProps.query, this.props.query)) {
      this.setState({ fellows: null });
      this.fetchFellows(this.props.query);
    }
  }

  hasQueryChanged(oldQuery, newQuery) {
    // compare the 2 query objects
    // see if they contain exactly the same key-value pairs
    let hasChanged = false;
    let newQKeys = Object.keys(newQuery);

    Object.keys(oldQuery).forEach(key => {
      if (newQuery[key] === undefined || oldQuery[key] !== newQuery[key]) {
        return true;
      }

      newQKeys.splice(newQKeys.indexOf(key), 1);
    });

    if (newQKeys.length) { // newQuery has more key-value pairs than oldQuery
      hasChanged = true;
    }

    return hasChanged;
  }

  renderFellowCard(fellow) {
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
      'custom_link': { text: `See work`, link: `https://${this.props.env.PULSE_DOMAIN}/profile/${fellow.profile_id}` }
    };

    return <Person metadata={metadata} key={fellow.name} />;
  }

  renderFellows() {
    if (!this.state.fellows) {
      return <div className="col-12 mx-auto my-5 text-center"><LoadingIndicator /></div>;
    }

    return this.state.fellows.length ? this.state.fellows.map(fellow => this.renderFellowCard(fellow)) : <div className="col-12 mb-5">No fellow profile found.</div>;
  }

  render() {
    return <div className="row fellow-list">{this.renderFellows()}</div>;
  }
}

FellowList.propTypes = {
  env: PropTypes.object.isRequired,
  query: PropTypes.object.isRequired
};
