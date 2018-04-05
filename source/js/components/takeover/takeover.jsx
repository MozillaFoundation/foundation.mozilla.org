import React from 'react';
import ReactGA from 'react-ga';

export default class Takeover extends React.Component {
  hide () {
    window.scrollTo(0, 0);

    this.setState({
      isHidden: true
    });

    ReactGA.event({
      category:`splash`,
      action: `splash exit`,
      label: `Preview from splash`
    });

    this.props.onHide.call();
  }

  constructor(props) {
    super(props);

    this.hide = this.hide.bind(this);
    this.logJoinBtn = this.logJoinBtn.bind(this);

    this.state = {
      isHidden: false
    };
  }

  logJoinBtn () {
    ReactGA.event({
      category:`splash`,
      action: `splash exit`,
      label: `Join from splash`
    });
  }

  render() {
    return (
      <div hidden={this.state.isHidden}>
        <header className="bar">
          <div className="container py-3">
            <img src="/_images/mozilla-on-black.svg" width="100"/>
          </div>
        </header>
        <div className="container">
          <div className="row">
            <div className="col-xs-12 col-md-9 py-3 py-md-5">
              <div className="my-3 my-md-5">
                <h1 className="h1-heading">This is a Barn Raising</h1>
              </div>

              <p>There is a movement to keep the Internet healthy taking root around the world. Mozilla is a part of this movement – and wants to help it grow.</p>
              <p>This site is part of our effort to do just that: a gathering place for people who care about the health of the Internet. A place to connect, tell stories, and find resources that will help us along the way.</p>
              <p>As of April 2017, this site is in "barn raising" mode. Building from the community that emerged around events like MozFest, we've started building a home for people working on Internet health might look like. This is our first pass and like any good open project we'll be iterating early and often.</p>
              <p>If you see yourself as part of this movement – or a part of Mozilla's community – we want your feedback, your ideas, and your help building this site. This is a barn raising.</p>
              <p>We plan to fully launch this site – and a network to support the movement – in the coming months.</p>
              <p className="h5-heading mb-0">Mark Surman</p>
              <p className="mb-0">Executive Director</p>
              <p>Mozilla</p>
            </div>
          </div>
        </div>
        <div className="button-group">
          <div className="container p-2">
            <button className="btn btn-normal" onClick={this.hide}>Preview Site</button>
            <a className="btn btn-ghost" onClick={this.logJoinBtn}
              href="/sign-up/">Join The Network</a>
          </div>
        </div>
      </div>
    );
  }
}
