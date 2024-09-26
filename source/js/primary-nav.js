let primaryNav = {
  init: function () {
    let elBurger = document.querySelector(`.burger`);
    let elNarrowMenu = document.querySelector(`.narrow-screen-menu`);
    let menuOpen = false;

    function setNarrowMenuState(openMenu) {
      if (openMenu) {
        elNarrowMenu.classList.remove(`hidden`);

        function handleTransitionEnd() {
          elNarrowMenu.focus();
          elNarrowMenu.removeEventListener(
            "transitionend",
            handleTransitionEnd
          );
        }
        elNarrowMenu.addEventListener("transitionend", handleTransitionEnd);
      } else {
        elNarrowMenu.classList.add(`hidden`);
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
        window.dataLayer.push({
          event: `show_navigation_menu`,
          category: `navigation`,
          action: `show menu`,
          label: `Show navigation menu`,
        });
      } else {
        window.dataLayer.push({
          event: `hide_navigation_menu`,
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
      toggleDonateBanner(openMenu);
      setNarrowMenuState(openMenu);
      setBurgerState(openMenu);
      trackMenuState(openMenu);
      setBodyHeight(openMenu);
    }

    // temporary hide the donate banner when the menu is open
    function toggleDonateBanner(hideDonateBanner) {
      const donateBanner = document.querySelector(`.donate-banner`);

      if (!donateBanner) {
        return;
      }

      if (hideDonateBanner) {
        donateBanner.classList.add(`tw-hidden`);
      } else {
        donateBanner.classList.remove(`tw-hidden`);
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
  },
};

export default primaryNav;
