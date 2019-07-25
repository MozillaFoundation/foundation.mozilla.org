import ReactGA from "react-ga";
import navNewsletter from "./nav-newsletter.js";

let primaryNav = {
  init: function() {
    let elBurger = document.querySelector(`.burger`);
    let elWideMenu = document.querySelector(`.wide-screen-menu`);
    let elNarrowMenu = document.querySelector(`.narrow-screen-menu`);
    let primaryNavContainer = document.getElementById(`primary-nav-container`);
    let navMode = primaryNavContainer.dataset.navMode;
    let menuOpen = false;

    function setWideMenuState(openMenu) {
      if (navMode === `zen`) {
        if (openMenu) {
          elWideMenu.classList.remove(`hidden`);
        } else {
          elWideMenu.classList.add(`hidden`);
        }
      }
    }

    function setNarrowMenuState(openMenu) {
      if (openMenu) {
        elNarrowMenu.classList.remove(`hidden`);
      } else {
        elNarrowMenu.classList.add(`hidden`);
      }
    }

    function setBurgerState(openMenu) {
      if (openMenu) {
        elBurger.classList.add(`menu-open`);
      } else {
        elBurger.classList.remove(`menu-open`);
      }
    }

    function trackMenuState(openMenu) {
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

    function setMenuState(openMenu) {
      setWideMenuState(openMenu);
      setNarrowMenuState(openMenu);
      setBurgerState(openMenu);
      trackMenuState(openMenu);
    }

    document.addEventListener(`keyup`, e => {
      if (e.keyCode === 27) {
        menuOpen = false;
        setMenuState(menuOpen);
      }
    });
    elBurger.addEventListener(`click`, () => {
      if (navNewsletter.getShownState()) {
        // if newsletter section is open, close just that section
        // instead of changing the menuOpen state
        navNewsletter.closeMobileNewsletter();
      } else {
        menuOpen = !menuOpen;
        setMenuState(menuOpen);
      }
    });
  }
};

export default primaryNav;
