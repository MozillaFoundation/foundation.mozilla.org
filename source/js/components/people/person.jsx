import React from 'react';

export default class Person extends React.Component {
  constructor(props) {
    super(props);
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
        if (this.props.metadata.links[key] !== `` && key !== `interview`) {
          filteredLinks[key] = this.props.metadata.links[key];
        }
      }
    }

    let socialLinks = Object.keys(filteredLinks).map((linkKey, index) => {
      let classes = `${linkKey} gray mr-4`;

      return (
        <a href={this.props.metadata.links[linkKey]} className={classes} key={index}></a>
      );
    });

    let metaBlock = (
      <div className="meta-block mb-2">
        <div className="h5-black mb-1">{this.props.metadata.name}</div>
        <div className="meta-block-item meta-block-item-role">{this.props.metadata.role}</div>
        <div className="meta-block-item meta-block-item-location">{this.props.metadata.location}</div>
      </div>
    );

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
            </div>
            <div className="col">
              <div className="row">
                <div ref="quoteContent" className="col-12 quote-content d-flex pt-3">
                  <div className="col">
                    <div className="row my-5">
                      <div className="person-quote quote-small">{this.props.metadata.quote}</div>
                    </div>
                    <div className="row">
                      <div className="quote-attribution">
                        {metaBlock}
                        <div className="person-issues mb-2">{issues}</div>
                        <div className="small-gray">{this.props.metadata.affiliations[0]}</div>
                        {this.props.metadata.partnership_logo &&
                          <div className="my-1">
                            <img className="partnership_logo" src={this.props.metadata.partnership_logo} alt="Logo of partnered organization"/>
                          </div>
                        }
                      </div>
                    </div>
                    <div className="row person-social-links mt-3 justify-content-between">
                      {socialLinks.length > 0 &&
                        <div>{socialLinks}</div>
                      }
                      {this.props.metadata.links.interview &&
                      <div>
                        <a className="cta-link" href={this.props.metadata.links.interview}>Read Interview</a>
                      </div>
                      }
                      {this.props.metadata.fellow_directory_link &&
                      <div>
                        <a href={this.props.metadata.fellow_directory_link.link} className="cta-link">See all {this.props.metadata.fellow_directory_link.type} fellows</a>
                      </div>
                      }
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
            </div>
            <div className="col bio-content pt-3">
              {metaBlock}
              <div className="person-issues">{issues}</div>
              <div className="person-affiliations small-gray mt-2">{this.props.metadata.affiliations.join(`; `)}</div>
              {this.props.metadata.partnership_logo &&
                <div className="row mt-3">
                  <div className="col">
                    <img className="partnership_logo" src={this.props.metadata.partnership_logo} alt="Logo of partnered organization"/>
                  </div>
                </div>
              }
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
