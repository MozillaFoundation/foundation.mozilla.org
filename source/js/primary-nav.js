import { ReactGA } from "./common";
import navNewsletter from "./nav-newsletter.js";

let primaryNav = {
  init: function () {
    let elBurger = document.querySelector(`.burger`);
    let elWideMenu = document.querySelector(`.wide-screen-menu`);
    let elNarrowMenu = document.querySelector(`.narrow-screen-menu`);
    let primaryNavContainer = document.querySelector(`.primary-nav-container`);
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
        elNarrowMenu.classList.add(`tw-z-50`);
      } else {
        elNarrowMenu.classList.add(`hidden`);
        elNarrowMenu.classList.remove(`tw-z-50`);
      }
    }

    function setBurgerState(openMenu) {
      if (openMenu) {
        elBurger.classList.add(`menu-open`);
        elBurger.setAttribute(`aria-label`, `Close menu`);
      } else {
        elBurger.classList.remove(`menu-open`);
        elBurger.setAttribute(`aria-label`, `Open menu`);
      }
    }

    function trackMenuState(openMenu) {
      if (openMenu) {
        ReactGA.event({
          category: `navigation`,
          action: `show menu`,
          label: `Show navigation menu`,
        });
      } else {
        ReactGA.event({
          category: `navigation`,
          action: `hide menu`,
          label: `Hide navigation menu`,
        });
      }
    }

    function setBodyHeight(openMenu) {
      // set body height and overflow to prevent scrolling on the body when mobile nav is open
      if (openMenu) {
        document.body.style.height = `100vh`;
        document.body.style.overflow = `hidden`;
      } else {
        document.body.style.height = `auto`;
        document.body.style.overflow = `auto`;
      }
    }

    function setMenuState(openMenu) {
      setWideMenuState(openMenu);
      setNarrowMenuState(openMenu);
      setBurgerState(openMenu);
      trackMenuState(openMenu);
      setBodyHeight(openMenu);
    }

    document.addEventListener(`keyup`, (e) => {
      if (e.keyCode === 27) {
        menuOpen = false;
        setMenuState(menuOpen);
      }
    });
    elBurger.addEventListener(`click`, () => {
      if (navNewsletter.isVisible()) {
        // if newsletter section is open, close just that section
        // instead of changing the menuOpen state
        navNewsletter.closeMobileNewsletter();
      } else {
        menuOpen = !menuOpen;
        setMenuState(menuOpen);
      }
    });
  },
};

export default primaryNav;
