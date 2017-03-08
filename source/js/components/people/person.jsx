import React from 'react';

export default class Person extends React.Component {
  constructor(props) {
    super(props);
    this.flip = this.flip.bind(this);

    this.state = {
      flipped: false
    };

  }

  flip() {
    this.setState({'flipped': !this.state.flipped});
  }

  render() {


    let issues = this.props.metadata.internet_health_issues.map((issue, index) => {
      return (
        <a href="#" key={index} className="link-small issue-link d-inline-block mr-1">{issue}</a>
      );
    });

    let socialLinks = Object.keys(this.props.metadata.links).map((linkKey, index) => {
      let classes = linkKey + ` mr-3`;

      return (
        <a href={this.props.metadata.links[linkKey]} className={classes} key={index}></a>
      );
    });

    if (this.props.metadata.featured) {
      return (
        <div className="col-12 p-3 mb-4">
          <div className="person-card person-card-featured row no-gutters">
            <div className="col-12 col-sm-4 mr-3">
              <div className="row">
                <div className="col">
                  <img src={this.props.metadata.image} alt="Headshot" />
                </div>
              </div>
              <div className="row">
                <div className="col">
                  <img className="partnership_logo" src={this.props.metadata.partnership_logo} alt="Logo of partnered organization"/>
                </div>
              </div>
            </div>
            <div className="col d-flex flex-column">
              <div className="justify-content-end row no-gutters">
                <div className="col col-auto" tabIndex="1" onClick={this.flip} >
                  <div className="background-left-slant more-details">{this.state.flipped?`MORE DETAILS +`:`SEE QUOTE +`}</div>
                </div>
              </div>
              <div className={`row flex-1 flippable-card flip-${this.state.flipped}`}>
                <div className="col-12 bio-content">
                  <h2 className="h5-black my-2">{this.props.metadata.name}</h2>
                  <div className="small">{this.props.metadata.role} / {this.props.metadata.location}</div>
                  <div className="person-issues">{issues}</div>
                  <div className="person-affiliations small-gray mt-2">{this.props.metadata.affiliations}</div>
                  <div className="person-bio body-black">
                    <ul>
                      {this.props.metadata.bio.map((item, index)=>{
                        console.log(item);
                        return (<li key={index}>{item}</li>);
                      })}
                    </ul>
                  </div>
                  <div className="person-social-links mt-3">
                    {socialLinks}
                  </div>
                </div>
                <div className="col-12 quote-content d-flex">
                  <div className="col d-flex flex-column flex-1">
                      <div className="row my-auto">
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
            <div className="col col-sm-4 mr-3">
              <img src={this.props.metadata.image} style={{"width":`100%`}} alt="Headshot" />
            </div>
            <div className="col bio-content">
              <h2 className="h5-black my-2">{this.props.metadata.name}</h2>
              <div className="small">{this.props.metadata.role} / {this.props.metadata.location}</div>
              <div className="person-issues">{issues}</div>
              <div className="person-affiliations small-gray mt-2">{this.props.metadata.affiliations}</div>
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
