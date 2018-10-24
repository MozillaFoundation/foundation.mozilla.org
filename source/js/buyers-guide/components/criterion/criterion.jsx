import React from 'react';

// Helper function to get the text content from
// a DOM element. Returns false if the query
// selector fails to find an element.
function getValueFrom(e, qs) {
  let v = e.querySelector(qs);
  return v ? v.textContent : false;
}

// These values are currently based on the list that is set up
// in networkapi/buyersguide/templates/tags/criterion.html
const PRODUCT_PROPERTIES = [
  `class`,
  `id`,
  `question`,
  `helptext`,
  `answer`
];

export default class Criterion extends React.Component {
  constructor(props) {
    super(props);

    let meta = {};

    PRODUCT_PROPERTIES.forEach(p => {
      meta[p] = getValueFrom(this.props.data, `.${p}`);
    });

    this.state = {
      hasHelptext: !!meta.helptext,
      helptextVisible: false,
      meta
    };
  }

  toggle() {
    this.setState({
      helptextVisible: !this.state.helptextVisible
    });
  }

  render() {
    let meta = this.state.meta;
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
          <p className="rating"><span dangerouslySetInnerHTML={{__html: meta.answer}}></span> <span className="emoji"></span></p>
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
