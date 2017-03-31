import React from 'react';
import ReactMarkdown from 'react-markdown';

export default class Person extends React.Component {
  constructor(props) {
    super(props);
    this.flip = this.flip.bind(this);

    this.state = {
      flipped: true
    };

  }

  flip() {
    if(this.state.flipped) {
      this.setState({
        'flippableStyle': {
          height: this.refs.bioContent.clientHeight
        }});
    } else {
      this.setState({
        'flippableStyle': {
          height: this.refs.quoteContent.clientHeight
        }});
    }
    this.setState({'flipped': !this.state.flipped});
  }

  componentDidMount() {
    this.refs.quoteContent && this.setState({'flippableStyle': {
      height: this.refs.quoteContent.clientHeight
    }});
  }

  render() {


    let issues = this.props.metadata.internet_health_issues.map((issue, index) => {
      return (
        <span key={index} className="issue-link small d-inline-block mr-1">{issue}</span>
      );
    });

    let filteredLinks = {};

    // Django returns empty strings instead of null for empty links, so let's filter empty links out:
    for(let key in this.props.metadata.links) {
      if (Object.prototype.hasOwnProperty.call(this.props.metadata.links, key)) {
        if (this.props.metadata.links[key] !== ``) {
          filteredLinks[key] = this.props.metadata.links[key];
        }
      }
    }

    let socialLinks = Object.keys(filteredLinks).map((linkKey, index) => {
      let classes = linkKey + ` mr-3`;

      return (
        <a href={this.props.metadata.links[linkKey]} className={classes} key={index}></a>
      );
    });

    if (this.props.metadata.featured) {
      return (
        <div className="col-12 p-3 mb-4">
          <div className="person-card person-card-featured row no-gutters">
            <div className="col-md-4 col-12 mr-3">
              <div className="row">
                <div className="col">
                  <img src={this.props.metadata.image} className="headshot" alt="Headshot" />
                </div>
              </div>
              {this.props.metadata.partnership_logo &&
                <div className="row mt-3">
                  <div className="col">
                    <img className="partnership_logo" src={this.props.metadata.partnership_logo} alt="Logo of partnered organization"/>
                  </div>
                </div>
              }
            </div>
            <div className="col d-flex flex-column">
              <div className="justify-content-end row no-gutters">
                <div className="col col-auto">
                  <button className="more-details btn" onClick={this.flip} >{this.state.flipped?`MORE DETAILS`:`SEE QUOTE`}</button>
                </div>
              </div>
              <div className={`row flippable-card flip-${this.state.flipped}`} style={this.state.flippableStyle}>
                <div ref="bioContent" style={this.state.bioStyle} className="col-12 bio-content">
                  <h2 className="h5-black my-2">{this.props.metadata.name}</h2>
                  <div className="person-role-location small">{this.props.metadata.role} / {this.props.metadata.location}</div>
                  <div className="person-issues">{issues}</div>
                  <div className="person-affiliations small-gray mt-2">{this.props.metadata.affiliations.join(`; `)}</div>
                  <div className="person-bio body-black">
                    <ReactMarkdown source={this.props.metadata.bio} />
                  </div>
                  <div className="person-social-links mt-3">
                    {socialLinks}
                  </div>
                </div>
                <div ref="quoteContent" style={this.state.quoteStyle} className="col-12 quote-content d-flex">
                  <div className="col d-flex flex-column flex-1">
                      <div className="row my-5">
                        <div className="person-quote quote-small">{this.props.metadata.quote}</div>
                      </div>
                      <div className="row justify-content-end">
                        <div className="quote-attribution text-right">
                          <div className="h5-black"> – {this.props.metadata.name}</div>
                          <div className="small">{this.props.metadata.role} / {this.props.metadata.location}</div>
                        </div>
                      </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    } else {
      return (
        <div className="col-md-6 col-12 p-3 mb-4">
          <div className="person-card row no-gutters">
            <div className="col-4 mr-3">
              <div className="row">
                <div className="col">
                  <img src={this.props.metadata.image} className="headshot" alt="Headshot" />
                </div>
              </div>
              {this.props.metadata.partnership_logo &&
                <div className="row mt-3">
                  <div className="col">
                    <img className="partnership_logo" src={this.props.metadata.partnership_logo} alt="Logo of partnered organization"/>
                  </div>
                </div>
              }
            </div>
            <div className="col bio-content">
              <h2 className="h5-black my-2">{this.props.metadata.name}</h2>
              <div className="small person-role-location">{this.props.metadata.role} / {this.props.metadata.location}</div>
              <div className="person-issues">{issues}</div>
              <div className="person-affiliations small-gray mt-2">{this.props.metadata.affiliations.join(`; `)}</div>
              <div className="person-social-links mt-3">
                {socialLinks}
              </div>
            </div>
          </div>
        </div>
      );
    }
  }
}
