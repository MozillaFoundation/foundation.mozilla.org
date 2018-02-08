import React from 'react';

export default class MultipageNav extends React.Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);

    this.state = {
      isOpen: false
    };
  }

  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }

  render() {
    let activeLinkLabel;
    let links = this.props.links.map((link, index) => {
      let className = `multipage-link${ link.isActive ? ` multipage-link-active` : `` }`;

      if (link.isActive) {
        activeLinkLabel = <a className={`active-link-label d-inline-block ${className}`}>{link.label}</a>;
      }

      return (
        <div key={`link-${index}`}>
          <a href={link.href} className={className}>{link.label}</a>
        </div>
      );
    });

    links.unshift(<div key="current-active-link">
      <button className="expander" onClick={this.toggle}>
        <div className="d-flex justify-content-between">
          {activeLinkLabel}
          <div className="d-inline-block control"></div>
        </div>
      </button>
    </div>);

    return (
      <div className={`multipage-nav${this.state.isOpen ? ` multipage-nav-open` : ``}`}>
        {links}
      </div>
    );
  }
}
