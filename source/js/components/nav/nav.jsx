import React from 'react';
import ReactGA from 'react-ga';

export default class PrimaryNav extends React.Component {
  show () {
    this.setState({
      isHidden: false
    });

    ReactGA.event({
      category: `navigation`,
      action: `show menu`,
      label: `Show navigation menu`
    });
  }

  hide () {
    this.setState({
      isHidden: true
    });

    ReactGA.event({
      category: `navigation`,
      action: `hide menu`,
      label: `Hide navigation menu`
    });
  }

  toggle () {
    if (this.state.isHidden) {
      this.show();
    } else {
      this.hide();
    }
  }

  componentDidUpdate () {
    if(this.props.onStateChange) {
      this.props.onStateChange.call(this, this.state);
    }
  }

  constructor(props) {
    super(props);

    this.hide = this.hide.bind(this);

    this.state = {
      isHidden: true
    };
  }

  render() {
    return (
      <header hidden={this.state.isHidden}>
        <div className="container">
          <div className="row p-4 d-flex justify-content-end">
            <button className="btn-close text-hide" onClick={this.hide}>X</button>
          </div>
          <div className="row d-md-flex justify-content-between">
            <div className="col-sm-auto align-self-end">
              <ul className="px-5 menu-nav">
                <li><a className="home" href="/">Home</a></li>
                <li><a className="people" href="/people">People</a></li>
                <li><a className="get-involved" href="/get-involved">Get Involved</a></li>
                <li><a className="projects" href="/projects">Projects</a></li>
                <li><a className="upcoming" href="/programs/upcoming">Upcoming</a></li>
                <li><a className="about" href="/about">About</a></li>
              </ul>
            </div>
          </div>
        </div>
      </header>
    );
  }
}
