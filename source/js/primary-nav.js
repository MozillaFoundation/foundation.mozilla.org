import ReactGA from "react-ga";

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
      menuOpen = !menuOpen;
      setMenuState(menuOpen);
    });

    // Newsletter Header Form

    let newsletterContainer = document.querySelector(".newsletter-header-form");
    let newsletterButtonSmall = document.getElementById("newsletter-button-2");
    let newsletterButtonLarge = document.getElementById("newsletter-button");
    let newsletterInput = document.getElementById("newsletter-input");

    function closeNewsletter(event) {
      if (
        !newsletterContainer.contains(event.target) &&
        event.target !== newsletterContainer
      ) {
        newsletterContainer.classList.remove("newsletter-active");
        newsletterButtonLarge.classList.remove("newsletter-button-active");
        document.removeEventListener("click", closeNewsletter);
      }
    }

    //Form at desktop+
    newsletterButtonLarge.addEventListener("click", event => {
      if (!newsletterContainer.classList.contains("newsletter-active")) {
        newsletterContainer.classList.add("newsletter-active");
        newsletterButtonLarge.classList.add("newsletter-button-active");
        newsletterInput.focus();
        event.stopPropagation();
        document.addEventListener("click", closeNewsletter);
      }
    });

    //Form at mobile & tablet
    newsletterButtonSmall.addEventListener("click", event => {
      event.preventDefault();
      newsletterContainer.style.height = "100%";
      document.querySelector(".narrow-screen-menu-container").style.display =
        "none";

      //need to close mobile & tablet form
    });
  }
};

export default primaryNav;
