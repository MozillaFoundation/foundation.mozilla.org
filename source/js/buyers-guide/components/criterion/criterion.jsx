import React from 'react';

export default class Criterion extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      hasHelptext: !!this.props.meta.helptext,
      helptextVisible: false
    };
  }

  toggle() {
    this.setState({
      helptextVisible: !this.state.helptextVisible
    });
  }

  render() {
    let meta = this.props.meta;
    let fullClass = `criterion criterion-${meta.class} criterion-${meta.id}`;

    return (
      <div className={fullClass}>
        <div className="primary-info">
          <p className="d-flex align-items-center">
            <span dangerouslySetInnerHTML={{__html: meta.question}}></span>
            {this.state.hasHelptext &&
              <button onClick={() => this.toggle()} className={this.state.helptextVisible ? `open` : `closed`}></button>
            }
          </p>
          <p className="rating">{ meta.answer } <span className="emoji"></span></p>
        </div>
        {this.state.helptextVisible &&
        <div className="helptext mt-3">
          {meta.helptext}
        </div>
        }
      </div>
    );
  }
}
