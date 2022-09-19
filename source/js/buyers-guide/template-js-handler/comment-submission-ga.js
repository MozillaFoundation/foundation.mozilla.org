/**
 * PNI product pages use commento to handle comment submissions.
 * This file adds a handler in order to fire a GA event if the user logs into commento and submits a comment.
 */
 export default () => {
    const menuBurger = document.querySelector(".burger");
    const primanyNavContainer = document.querySelector(
      ".primary-nav-container-wrapper"
    );
  
    if (!menuBurger || !primanyNavContainer) return;
  
    const classToDetect = "menu-open";
    const classToToggle = "sticky-top";
    let prevMenuState = menuBurger.classList.contains(classToDetect);
    const mutationHandler = (mutations) => {
      mutations.forEach(function (mutation) {
        if (mutation.attributeName === "class") {
          let currentMenuState =
            mutation.target.classList.contains(classToDetect);
          if (prevMenuState !== currentMenuState) {
            prevMenuState = currentMenuState;
            if (currentMenuState) {
              primanyNavContainer.classList.add(classToToggle);
            } else {
              primanyNavContainer.classList.remove(classToToggle);
            }
          }
        }
      });
    };
  
    const mobileMenuObserver = new MutationObserver(mutationHandler);
    mobileMenuObserver.observe(menuBurger, { attributes: true });
  };
  