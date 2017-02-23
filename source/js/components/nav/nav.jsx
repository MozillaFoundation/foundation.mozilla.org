import React from 'react';

export default class PrimaryNav extends React.Component {
  show () {
    this.setState({
      isHidden: false
    });
  }

  hide () {
    this.setState({
      isHidden: true
    });
  }

  toggle () {
    this.setState({
      isHidden: !this.state.isHidden
    });
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
          <div className="row p-4">
            <button className="btn-close text-hide" onClick={this.hide}>X</button>
          </div>
          <div className="row d-flex justify-content-between">
            <div className="col align-self-end">
              <ul className="px-5 menu-nav">
                <li><a href="/">Home</a></li>
                <li><a href="/people">People</a></li>
                <li><a href="/programs">Programs</a></li>
                <li><a href="/projects">Projects</a></li>
                <li><a href="/campaigns">Campaigns</a></li>
                <li><a href="/programs/upcoming">Upcoming</a></li>
                <li><a href="/about">About</a></li>
              </ul>
            </div>
            <div className="col pb-3 px-3 align-self-end flex-grow-0">
              <ul className="pb-2 menu-nav menu-nav-side">
                <li><a className="d-flex align-items-center twitter" href="https://twitter.com/mozilla">Twitter</a></li>
                <li><a className="d-flex align-items-center chat" href="#TODO">Chat</a></li>
                <li><a className="d-flex align-items-center email" href="#TODO">Email</a></li>
                <li><a className="d-flex align-items-center donate" href="https://donate.mozilla.org">Donate</a></li>
                <li><em><a style={{color:`yellow`}} href="/style-guide">Style Guide</a></em></li>
              </ul>
              <a href="https://mozilla.org" className="text-hide logo">Mozilla</a>
            </div>
          </div>
        </div>
      </header>
    );
  }
}
