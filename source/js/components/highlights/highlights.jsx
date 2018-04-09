import React from 'react';
import PropTypes from 'prop-types';

export default class Highlights extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    let superHighlights = this.props.data.slice(0, 2).map((item, index) => {
      return (
        <div className="col-md-6" key={`super-highlight-${index}`}>
          <div className={`${item.image ? `pb-5` : `py-5`}`}>
            { item.image &&
              <img src={item.image} />
            }
            <div className="key-item mx-2 mx-md-4 p-3">
              <h5 className="h4-heading mb-2">{item.title}</h5>
              <p>{item.description}</p>
              <a className="cta-link mb-2" href={item.link_url}>{item.link_label}</a>
            </div>
          </div>
        </div>
      );
    });

    let highlights = this.props.data.slice(2).map((item, index) => {
      return (
        <div className="row my-3" key={`highlight-${index}`}>
          <div className="col-sm-12 col-md-4 pt-3 hidden-sm-down">
            { item.image ? <img src={item.image}/> : <div className="placeholder"></div> }
          </div>
          <div className="col-sm-12 col-md-8 pt-3">
            { index !== 0 && <hr className="mt-0 mb-4" /> }
            <h5 className="h5-heading mb-3"><a href={item.link_url}>{item.title}</a></h5>
            <p>{item.description}</p>
          </div>
        </div>
      );
    });

    return (
      <div className="highlights mb-5">
        <div className="row">
          {superHighlights}
        </div>
        {highlights}
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
