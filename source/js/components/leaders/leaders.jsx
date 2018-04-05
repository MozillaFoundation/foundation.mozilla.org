import React from 'react';
import PropTypes from 'prop-types';

export default class Leaders extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    // Limit to 4 leaders
    let leaders = this.props.data.slice(0, 4).map((item, index) => {
      return (
        <div className="featured-person col-6 col-sm-4 col-md-3 mb-4 mb-sm-0" key={index}>
          <img className="img-fluid d-block" src={item.image} alt="Headshot"/>
          <h2 className="h5-heading my-2">{item.name}</h2>
          <p className="small-gray">{item.affiliations.join(`, `)}</p>
          <div className="person-social-links mt-3">
            { item.links.twitter && <a href={item.links.twitter} className="twitter gray small mr-4"></a> }
            { item.links.linkedIn && <a href={item.links.linkedIn} className="linkedIn gray small mr-4"></a> }
          </div>
        </div>
      );
    });

    return (
      <div className="row">
        { leaders }
      </div>
    );
  }
}

Leaders.propTypes = {
  data: PropTypes.array
};

Leaders.defaultProps = {
  data: []
};
