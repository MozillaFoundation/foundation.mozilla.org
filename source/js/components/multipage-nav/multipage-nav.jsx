import React from 'react';

export default class MultipageNav extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    let links = this.props.links.map((link, index) => {
      let className = `opp-link${ link.isActive ? ` opp-link-active` : `` }`;

      return (
        <div key={`link-${index}`}>
          <a href={link.href} className={className}>{link.label}</a>
        </div>
      );
    });

    return (
      <div className="multipage-nav">
        {links}
      </div>
    );
  }
}
