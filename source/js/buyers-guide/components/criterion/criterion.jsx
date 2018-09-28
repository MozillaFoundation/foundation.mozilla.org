import React from 'react';

export default class Criterion extends React.Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);

    this.state = {
      hasHelptext: this.props.meta.helptext.length > 0,
      helptextVisible: false
    };
  }

  toggle() {
    this.setState({
      helptextVisible: !this.state.helptextVisible
    });
  }

  render() {
    let fullClass = `criterion criterion-${this.props.meta.class} criterion-${this.props.meta.id}`;

    return (
      <div className={fullClass}>
        <div className="primary-info">
          <p className="d-flex align-items-center">
            <span dangerouslySetInnerHTML={{__html:this.props.meta.question}}></span>
            {this.state.hasHelptext &&
              <button onClick={this.toggle} className={this.state.helptextVisible ? `open` : `closed`}></button>
            }
          </p>
          <p className="rating">{ this.props.meta.answer } <span className="emoji"></span></p>
        </div>
        {this.state.helptextVisible &&
        <div className="helptext mt-3">
          {this.props.meta.helptext}
        </div>
        }
      </div>
    );
  }
}
