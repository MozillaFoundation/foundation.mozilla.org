/*
* This is a modified version of source/js/primary-nav.js
*/

let primaryNav = {
  init: function() {
    let elBurger = document.querySelector(`.burger`);
    let elNarrowMenu = document.querySelector(`.narrow-screen-menu`);
    let elUnderneath = document.querySelector(`.underneath-screen-overlay`);
    let menuOpen = false;

    function setNarrowMenuState(openMenu) {
      if (openMenu) {
        elNarrowMenu.classList.add(`menu-open`);
      } else {
        elNarrowMenu.classList.remove(`menu-open`);
      }
    }

    function setBurgerState(openMenu) {
      if (openMenu) {
        elBurger.classList.add(`menu-open`);
      } else {
        elBurger.classList.remove(`menu-open`);
      }
    }

    function setContentUnderneathState(openMenu) {
      if (openMenu) {
        elUnderneath.classList.add(`menu-open`);
      } else {
        elUnderneath.classList.remove(`menu-open`);
      }
    }

    function setMenuState(openMenu) {
      setNarrowMenuState(openMenu);
      setBurgerState(openMenu);
      setContentUnderneathState(openMenu);
    }

    document.addEventListener(`keyup`, (e) => {
      if (e.keyCode === 27) {
        menuOpen = false;
        setMenuState(menuOpen);
      }
    });

    elBurger.addEventListener(`click`, () => {
      menuOpen = !menuOpen;
      setMenuState(menuOpen);
    });
  }
};

export default primaryNav;
