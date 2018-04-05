import React from 'react';

export default class MemberNotice extends React.Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);

    this.state = {
      isExpanded: false
    };
  }

  toggle() {
    // Just controls animation on +/x indicator
    this.setState({
      isExpanded: !this.state.isExpanded
    });

    let onTransitionEnd = () => {
      this.refs.wrapper.removeEventListener(`transitionend`, onTransitionEnd);

      this.removeMeasurements();

      if (this.state.isExpanded) {
        this.refs.pane2.classList.remove(`pane-hidden`);
      } else {
        this.refs.pane1.classList.remove(`pane-hidden`);
      }
    };

    this.refs.wrapper.addEventListener(`transitionend`, onTransitionEnd);

    this.setMeasurements();

    this.refs.pane1.classList.add(`pane-hidden`);
    this.refs.pane2.classList.add(`pane-hidden`);
  }

  // Allow the elements to scale normally (eg: If the window is resized)
  removeMeasurements() {
    this.refs.pane1.style.width = `auto`;
    this.refs.pane2.style.width = `auto`;
    this.refs.wrapper.style.height = `auto`;
  }

  // Force specific dimensions for smooth height transition
  setMeasurements() {
    let wrapperWidth = this.refs.wrapper.clientWidth;

    this.refs.pane1.style.width = `${wrapperWidth}px`;
    this.refs.pane2.style.width = `${wrapperWidth}px`;

    // Set "start" height (which is actually just the current height, but not explicitly set)
    this.refs.wrapper.style.height = this.state.isExpanded ? `${this.refs.pane2.clientHeight}px` : `${this.refs.pane1.clientHeight}px`;

    // Set "end" height (this triggers the transition to start)
    this.refs.wrapper.style.height = this.state.isExpanded ? `${this.refs.pane1.clientHeight}px` : `${this.refs.pane2.clientHeight}px`;
  }

  render() {
    return (
      <div className="container d-flex py-3 justify-content-between align-items-top">
        <div ref="wrapper" className="wrapper align-self-center mr-3">
          <div ref="pane1" className="pane">
            <p className="body-black mb-0">Welcome to our member preview. It’s a work in progress and we invite your <a href="https://mzl.la/2ohCL8O">feedback</a>.</p>
          </div>
          <div ref="pane2" className="pane pane-hidden">
            <div className="hidden-sm-down">
              <h3 className="h5-heading">This is a Barn Raising</h3>
              <p className="body-black">There is a movement to keep the Internet healthy taking root around the world. Mozilla is a part of this movement and wants to help it grow.</p>
              <p className="body-black">We're building a home for people who care about the health of the Internet, hand in hand with the community that emerged from MozFest and events around the world. It’s a space for us to learn, find resources, and connect to new people and ideas.</p>
              <p className="body-black mb-0">If you are a part of this movement for Internet Health then we want your <a href="https://mzl.la/2ohCL8O">feedback</a> to help it grow. This is a barn raising.</p>
            </div>
            <div className="hidden-md-up">
              <h3 className="h5-heading">This is a Movement</h3>
              <p className="body-black mb-0">We're building a home for people who care about the health of the Internet. This is a space for us to learn, find resources, and connect. If you're a part of the movement for Internet Health, we want your <a href="https://mzl.la/2ohCL8O">feedback</a> and help.</p>
            </div>
          </div>
        </div>
        <div>
          <button className={`btn btn-${this.state.isExpanded ? `expanded` : `collapsed`}`} onClick={this.toggle}>+</button>
        </div>
      </div>
    );
  }
}
