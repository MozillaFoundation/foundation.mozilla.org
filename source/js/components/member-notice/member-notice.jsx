import React from 'react';

export default class Takeover extends React.Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);

    this.state = {
      isExpanded: false
    };
  }

  toggle() {
    this.setState({
      isExpanded: !this.state.isExpanded
    });
  }

  render() {
    return (
      <div className="container d-flex py-3 justify-content-between align-items-top">
        <div className="align-self-center pr-3">
          <div className={`pane${this.state.isExpanded ? ` pane-hidden` : ``}`}>
            <p className="body-black mb-0">Welcome to our member preview. It’s a work in progress and we invite your <a href="https://mzl.la/2ohCL8O">feedback</a>.</p>
          </div>
          <div className={`pane${!this.state.isExpanded ? ` pane-hidden` : ``}`}>
            <h3 className="h5-black">This is a Barn Raising</h3>
            <p className="body-black">There is a movement to keep the Internet healthy taking root around the world. Mozilla is a part of this movement and wants to help it grow.</p>
            <p className="body-black">We're building a home for people who care about the health of the Internet, hand in hand with the community that emerged from MozFest and events around the world. It’s a space for us to learn, find resources, and connect to new people and ideas.</p>
            <p className="body-black">If you are a part of this movement for Internet Health then we want your <a href="https://mzl.la/2ohCL8O">feedback</a> to help it grow. This is a barn raising.</p>
          </div>
        </div>
        <div>
          <button className={`btn btn-${this.state.isExpanded ? `expanded` : `collapsed`}`} onClick={this.toggle}>+</button>
        </div>
      </div>
    );
  }
}
