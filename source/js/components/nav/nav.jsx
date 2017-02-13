import React from 'react';

export default class PrimaryNav extends React.Component {
  show () {
    console.log(`show`);

    this.setState({
      isHidden: false
    });
  }

  hide () {
    console.log(`hide`);

    this.setState({
      isHidden: true
    });
  }

  toggle () {
    this.setState({
      isHidden: !this.state.isHidden
    });
  }

  constructor(props) {
    super(props);

    this.state = {
      isHidden: true
    };
  }

  render() {
    return (
      <header hidden={this.state.isHidden} className="container py-2 mb-1">
        <p className="text-center"><a href="/"><img src="/_images/mozilla-wordmark.svg" style={{width:`150px`}}/></a></p>
        <ul className="py-3">
          <li><a href="/people">People</a></li>
          <li><a href="/programs">Programs</a>
            <ul>
              <li><a href="/programs/upcoming">Upcoming</a></li>
            </ul>
          </li>
          <li><a href="/projects">Projects</a></li>
          <li><a href="/campaigns">Campaigns</a></li>
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
      </header>
    );
  }
}
