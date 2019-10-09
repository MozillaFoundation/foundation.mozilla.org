import ReactGA from "react-ga";
import utility from "./utility";
import navNewsletter from "./nav-newsletter.js";

let elements = {
  elBurger: `.burger`,
  elWideMenu: `.wide-screen-menu`,
  elNarrowMenu: `.narrow-screen-menu`,
  primaryNavContainer: `#primary-nav-container`
};

class PrimaryNav {
  constructor() {
    this.navMode = null;
    this.menuOpen = false;
  }

  setWideMenuState(openMenu) {
    if (this.navMode === `zen`) {
      if (openMenu) {
        elements.elWideMenu.classList.remove(`hidden`);
      } else {
        elements.elWideMenu.classList.add(`hidden`);
      }
    }
  }

  setNarrowMenuState(openMenu) {
    if (openMenu) {
      elements.elNarrowMenu.classList.remove(`hidden`);
    } else {
      elements.elNarrowMenu.classList.add(`hidden`);
    }
  }

  setBurgerState(openMenu) {
    if (openMenu) {
      elements.elBurger.classList.add(`menu-open`);
    } else {
      elements.elBurger.classList.remove(`menu-open`);
    }
  }

  trackMenuState(openMenu) {
    if (openMenu) {
      ReactGA.event({
        category: `navigation`,
        action: `show menu`,
        label: `Show navigation menu`
      });
    } else {
      ReactGA.event({
        category: `navigation`,
        action: `hide menu`,
        label: `Hide navigation menu`
      });
    }
  }

  setMenuState(openMenu) {
    this.setWideMenuState(openMenu);
    this.setNarrowMenuState(openMenu);
    this.setBurgerState(openMenu);
    this.trackMenuState(openMenu);
  }

  init() {
    if (!utility.checkAndBindDomNodes(elements)) {
      return;
    }

    this.navMode = elements.primaryNavContainer.dataset.navMode;

    document.addEventListener(`keyup`, event => {
      this.docKeyupHanlder(event);
    });

    elements.elBurger.addEventListener(`click`, () => {
      this.elBurgerClickHanlder();
    });
  }

  docKeyupHanlder(event) {
    if (event.keyCode === 27) {
      this.menuOpen = false;
      this.setMenuState(this.menuOpen);
    }
  }

  elBurgerClickHanlder() {
    if (navNewsletter.getShownState()) {
      // if newsletter section is open, close just that section
      // instead of changing the menuOpen state
      navNewsletter.closeMobileNewsletter();
    } else {
      this.menuOpen = !this.menuOpen;
      this.setMenuState(this.menuOpen);
    }
  }
}

const primaryNav = new PrimaryNav();

export default primaryNav;
