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
        <div className="container p-4">
          <button onClick={this.hide}>X</button>
          <p className="text-center"><a href="/"><img src="/_images/logo.svg" style={{width:`150px`}}/></a></p>
          <ul className="py-3 menu-nav">
            <li><a href="/people">People</a></li>
            <li><a href="/programs">Programs</a></li>
            <li><a href="/projects">Projects</a></li>
            <li><a href="/campaigns">Campaigns</a></li>
            <li><a href="/programs/upcoming">Upcoming</a></li>
            <li><a href="/about">About</a></li>
          </ul>
          <ul className="pb-2">
            <li><a href="#TODO">Twitter</a></li>
            <li><a href="#TODO">Internet Health</a></li>
            <li><a href="#TODO">Email Us</a></li>
            <li><a href="#TODO">Donate</a></li>
          </ul>
          <ul className="pb-2">
            <li><em><a href="/style-guide">Style Guide</a></em></li>
          </ul>
        </div>
      </header>
    );
  }
}
