/*
* This is a slightly simplied version of source/js/primary-nav.js
*/

let primaryNav = {
  init: function() {
    let elBurger = document.querySelector(`.burger`);
    let elNarrowMenu = document.querySelector(`.narrow-screen-menu`);
    let elUnderneath = document.querySelector(`.underneath-screen-overlay`);
    let menuOpen = false;

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

    function setMenuState(openMenu) {
      setNarrowMenuState(openMenu);
      setBurgerState(openMenu);

      if (openMenu) {
        elUnderneath.style.display = `none`;
      } else {
        elUnderneath.style.display = `initial`;
      }
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
