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
    let newsletterButtonSmall = document.getElementById("newsletter-button-2"); // Mobile Button
    let newsletterButtonLarge = document.getElementById("newsletter-button"); // Tablet & Desktop Button
    let newsletterDismiss = document.querySelector(".form-dismiss");
    let newsletterInput = document.getElementById("newsletter-input");

    // Close form at desktop+
    function closeNewsletter(event) {
      if (
        !newsletterContainer.contains(event.target) &&
        event.target !== newsletterContainer
      ) {
        newsletterContainer.classList.remove("newsletter-active");
        newsletterButtonLarge.classList.remove("newsletter-button-active");
        document.removeEventListener("click", closeNewsletter);
        document.removeEventListener("scroll", closeNewsletter);
      }
    }

    // Open form at desktop+
    newsletterButtonLarge.addEventListener("click", event => {
      if (!newsletterContainer.classList.contains("newsletter-active")) {

        //Opens Newsletter Form & forces button's active state
        newsletterContainer.classList.remove('newsletter-low-opacity');
        newsletterContainer.classList.add("newsletter-active");
        newsletterButtonLarge.classList.add("newsletter-button-active");
        newsletterInput.focus();
        event.stopPropagation();

        //Listens for user's click or scroll to close newsletter

        document.addEventListener("click", closeNewsletter);
        document.addEventListener("scroll", closeNewsletter);
        
      }
    });

    //Close Mobile Form & bringing back nav

    function closeMobileNewsletter() {
      if (event.target == newsletterDismiss) {
        document.querySelector(".narrow-screen-menu-container").classList.remove('d-none');
        newsletterContainer.classList.replace('newsletter-full-opacity', 'newsletter-low-opacity');
      }
    }

    // Open form at mobile
    newsletterButtonSmall.addEventListener("click", () => {
      document.querySelector(".narrow-screen-menu-container").classList.add(`d-none`);
      newsletterContainer.classList.replace('newsletter-low-opacity', 'newsletter-full-opacity');

      newsletterDismiss.addEventListener('click', closeMobileNewsletter);
    });
  }
};

export default primaryNav;
