import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';

export default class Upcoming extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      events: []
    };
  }

  componentDidMount() {
    let networkSiteUrl = this.props.env.NETWORK_SITE_URL;

    // HEROKU_APP_DOMAIN is used by review apps
    if (!networkSiteUrl && this.props.env.HEROKU_APP_NAME) {
      networkSiteUrl = `https://${this.props.env.HEROKU_APP_NAME}.herokuapp.com`;
    }

    let xhr = new XMLHttpRequest();

    xhr.addEventListener(`load`, () => {
      this.setState({
        events: JSON.parse(xhr.response)
      });
    });

    xhr.open(`GET`, `${networkSiteUrl}/api/milestones/`);
    xhr.send();
  }

  render() {
    let data = this.state.events;

    let futureEvents = data.filter((event) => {
      return event.start_date === null || moment(event.start_date).isSameOrAfter(Date.now(), `month`);
    });

    // Sort chronologically
    futureEvents.sort((a, b) => {
      return new Date(a.start_date) - new Date(b.start_date);
    });

    let pastEvents = data.filter((event) => {
      return moment(event.start_date).isBefore(Date.now(), `month`);
    });

    // Sort reverse-chronologically
    pastEvents.sort((a, b) => {
      return new Date(b.start_date) - new Date(a.start_date);
    });

    let buildEvent = (meta, key) => {
      let displayDate;

      if(moment(meta.start_date).date() === 1 && moment(meta.end_date).date() === moment(meta.end_date).endOf(`month`).date()) {
        // Only show Month for events that span entire month
        displayDate = moment(meta.start_date).format(`MMMM, YYYY`);
      } else if(meta.start_date && meta.end_date && meta.start_date !== meta.end_date) {
        // Events that span a few days, but not a whole month
        displayDate = `${moment(meta.start_date).format(`MMMM D`)}-${moment(meta.end_date).format(`D, YYYY`)}`;
      } else if(meta.start_date) {
        // Single day events
        displayDate = moment(meta.start_date).format(`MMMM D, YYYY`);
      } else {
        // Events missing dates
        displayDate = `TBD`;
      }

      return (
        <div className="row my-5" key={key}>
          <div className="col-sm-4">
            { meta.photo && <img src={meta.photo}/> }
          </div>
          <div className="col-sm-8">
            <p className="h6-gray mt-3 mt-sm-0">{displayDate}</p>
            <h2 className="h4-light-black">{meta.headline}</h2>
            <p className="body-black">{meta.description}</p>
            <a className="cta-link" href={meta.link_url}>{meta.link_label}</a>
          </div>
        </div>
      );
    };

    futureEvents = futureEvents.map((item, index) => {
      return buildEvent(item, `fe-${index}`);
    });

    pastEvents = pastEvents.map((item, index) => {
      return buildEvent(item, `pe-${index}`);
    });

    return (
      <div className="container">
        { futureEvents }
        <div className="row">
          <div className="col">
            <hr className="hr-gradient"/>
            <h3 className="h2-headings-white">Recent</h3>
          </div>
        </div>
        { pastEvents }
      </div>
    );
  }
}

Upcoming.propTypes = {
  data: PropTypes.array
};

Upcoming.defaultProps = {
  data: []
};
