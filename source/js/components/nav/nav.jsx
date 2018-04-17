import React from 'react';
import ReactGA from 'react-ga';
import classNames from 'classnames';

export default class PrimaryNav extends React.Component {
  showMenu () {
    this.setState({
      menuOpen: true
    });

    ReactGA.event({
      category: `navigation`,
      action: `show menu`,
      label: `Show navigation menu`
    });
  }

  hideMenu () {
    this.setState({
      menuOpen: false
    });

    ReactGA.event({
      category: `navigation`,
      action: `hide menu`,
      label: `Hide navigation menu`
    });
  }

  toggleMenu () {
    if (this.state.menuOpen) {
      this.hideMenu();
    } else {
      this.showMenu();
    }
  }

  constructor(props) {
    super(props);

    this.hideMenu = this.hideMenu.bind(this);
    this.showMenu = this.showMenu.bind(this);
    this.toggleMenu = this.toggleMenu.bind(this);
    this.escKeyPressed = this.escKeyPressed.bind(this);

    this.state = {
      menuOpen: false
    };
  }

  escKeyPressed(e) {
    if (e.keyCode === 27) {
      this.hideMenu();
    }
  }

  componentDidMount() {
    // Close primary nav when escape is pressed
    document.addEventListener(`keyup`, this.escKeyPressed);
  }

  componentWillUnmount() {
    document.removeEventListener(`keyup`, this.escKeyPressed);
  }

  renderBurger() {
    let className = classNames(`burger`, {
      'hidden-md-up': this.props.navMode !== `zen`,
      'menu-open': this.state.menuOpen
    });

    return (
      <button onClick={this.toggleMenu} className={className}>
        <div className="burger-bar burger-bar-top"></div>
        <div className="burger-bar burger-bar-middle"></div>
        <div className="burger-bar burger-bar-bottom"></div>
      </button>
    );
  }

  renderNavLinks() {
    return [
      <a className="nav-link-initiatives" href="/initiatives">Initiatives</a>,
      <a className="nav-link-participate" href="/participate">Participate</a>,
      <a href="https://internethealthreport.org" target="_blank" rel="noopener noreferrer">Internet&nbsp;Health</a>,
      <a className="nav-link-people" href="/people">People</a>,
      <a className="nav-link-about" href="/about">About&nbsp;Us</a>
    ];
  }

  renderWideMenu() {
    let classsName = classNames(`nav-links hidden-sm-down`, {
      'hidden': this.props.navMode === `zen` && !this.state.menuOpen
    });

    return (
      <div className={classsName}>
        {this.renderNavLinks()}
      </div>
    );
  }

  renderNarrowMenu() {
    let classsName = classNames(`narrow-screen-menu`, {
      'hidden': !this.state.menuOpen
    });

    return (
      <div className={classsName}>
        <div className="narrow-screen-menu-background">
          <div className="nav-links">
            <a className="nav-link-home" href="/">Home</a>
            {this.renderNavLinks()}
          </div>
        </div>
      </div>
    );
  }

  render() {
    return (
      <div className="wrapper-burger">
        {this.renderNarrowMenu()}
        <div className="wide-screen-menu">
          <div className="container-fluid">
            <div className="row">
              <div className="col">
                <div className="d-flex flex-row justify-content-between">
                  <div className="py-sm-3 py-3 py-md-2 d-flex align-items-center flex-wrap">
                    {this.renderBurger()}
                    <a className="logo text-hide" href="/">
                      Mozilla Foundation
                    </a>
                    {this.renderWideMenu()}
                  </div>
                  <div>
                    <a id="donate-header-btn"
                      className="my-md-0 my-3 btn btn-pop"
                      href="https://donate.mozilla.org?utm_source=foundation.mozilla.org&utm_medium=referral&utm_content=header"
                      target="_blank" rel="noopener noreferrer"
                    >
                      Donate
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
