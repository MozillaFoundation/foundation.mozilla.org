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

    // Newsletter Section

    let newsletterContainer = document.querySelector(".nav-newsletter-form-wrapper");
    let newsletterDismiss = newsletterContainer.querySelector(".form-dismiss");
    let narrowMenuContainer = primaryNavContainer.querySelector(".narrow-screen-menu-container");
    let desktopMenuContainer = primaryNavContainer.querySelector(".wide-screen-menu-container");
    let newsletterButtonMobile = narrowMenuContainer.querySelector(".btn-newsletter");
    let newsletterButtonDesktop = desktopMenuContainer.querySelector(".btn-newsletter");
    let mobileNewsletterOpen = false;
    // let newsletterInput = document.getElementById("newsletter-input");

    let closeFormClickHandler = event => {
      // close newsletter section if clicking anywhere outside of the section
      if (
        !newsletterContainer.contains(event.target) &&
        event.target !== newsletterContainer
      ) {
        closeDesktopNewsletter();
      }
    };

    function expandDesktopNewsletter() {
      newsletterContainer.classList.add("expanded");
      newsletterButtonDesktop.classList.add("active");
    }

    function closeDesktopNewsletter() {
      newsletterContainer.classList.remove("expanded");
      newsletterButtonDesktop.classList.remove("active");
      document.removeEventListener("click", closeFormClickHandler);
    }

    // Open form at desktop+
    newsletterButtonDesktop.addEventListener("click", event => {
      if (!newsletterContainer.classList.contains("expanded")) {
        event.stopPropagation();

        expandDesktopNewsletter();
        document.addEventListener(`click`, closeFormClickHandler);
      }
    });

    function toggleMobileNewsletter() {
      if (!mobileNewsletterOpen) {
        // show newsletter form & hide nav
        narrowMenuContainer.classList.add(`d-none`);
        newsletterContainer.classList.add("faded-in");
        mobileNewsletterOpen = true;
      } else {
        // close newsletter form & bring back nav
        narrowMenuContainer.classList.remove("d-none");
        newsletterContainer.classList.remove("faded-in");
        mobileNewsletterOpen = false;
      }
    }

    newsletterButtonMobile.addEventListener("click", () => {
      toggleMobileNewsletter();
    });

    newsletterDismiss.addEventListener("click", () => {
      toggleMobileNewsletter();
    });
  }
};

export default primaryNav;
