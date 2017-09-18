import React from 'react';

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
          { index < array.length && <hr/> }
        </div>
      );
    });

    return (
      <div className="row">
        <div className="col-xs-12 col-md-6 mb-5">
          <div className={`item-featured px-4 ${this.props.data[0].image ? `mt-4 pb-5` : `py-5`}`}>
            { this.props.data[0].image &&
              <img className="key-item mb-4" src={this.props.data[0].image} />
            }
            <h5 className="h4-light-black">{this.props.data[0].title}</h5>
            <p className="body-black">{this.props.data[0].description}</p>
            <a className="cta-link" href={this.props.data[0].link_url}>{this.props.data[0].link_label}</a>
            <div className="mt-5"></div>
          </div>
        </div>
        <div className="col-md-6 mb-5">
          {highlights}
        </div>
      </div>
    );
  }
}
