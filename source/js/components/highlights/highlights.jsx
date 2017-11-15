import React from 'react';
import PropTypes from 'prop-types';

export default class Highlights extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    // Limit to 2 additional highlights
    let highlights = this.props.data.slice(1, 3).map((item, index, array) => {
      return (
        <div key={index}>
          <h5 className="h4-light-black">{item.title}</h5>
          <p className="body-black">{item.description}</p>
          <a className="cta-link" href={item.link_url}>{item.link_label}</a>
          { index < array.length - 1 && <hr/> }
        </div>
      );
    });

    let data = this.props.data[0];

    return (
      <div className="row">
        <div className="col-xs-12 col-md-6 mb-5">
          <div className={`${data.image ? `pb-5` : `py-5`}`}>
            { data.image &&
              <img src={data.image} />
            }
            <div className="key-item mx-2 mx-md-4 p-3">
              <h5 className="h4-light-black">{data.title}</h5>
              <p className="body-black">{data.description}</p>
              <a className="cta-link mb-2" href={data.link_url}>{data.link_label}</a>
            </div>
          </div>
        </div>
        <div className="col-md-6 mb-5">
          {highlights}
        </div>
      </div>
    );
  }
}

Highlights.propTypes = {
  data: PropTypes.array
};

Highlights.defaultProps = {
  data: []
};
