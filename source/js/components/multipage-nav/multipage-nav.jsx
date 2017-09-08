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
    let links = this.props.links.map((link, index) => {
      let className = `opp-link${ link.isActive ? ` opp-link-active` : `` }`;

      return (
        <div key={`link-${index}`}>
          <a href={link.href} className={className}>{link.label}</a>
          {index === 0 &&
            <button className="expander" onClick={this.toggle}></button>
          }
        </div>
      );
    });

    return (
      <div className={`multipage-nav${this.state.isOpen ? ` multipage-nav-open` : ``}`}>
        {links}
      </div>
    );
  }
}
