/**
 * PNI has special nav stickiness needs than the rest of the site.
 * (e.g., we want the category nav to be sticky but not the primary nav)
 * Without making primary-nav.js more complicated just to handle this special case,
 * we use MutationObserver to detect PNI's mobile menu's close/open state
 * so we can toggle class on .primary-nav-container-wrapper to
 * achieve the visual effects we want.
 */
export default () => {
  const menuBurger = document.querySelector(".burger");
  const primaryNavContainer = document.querySelector(
    ".primary-nav-container-wrapper"
  );

  if (!menuBurger || !primaryNavContainer) return;

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
            primaryNavContainer.classList.add(classToToggle);
            document
              .querySelector("#pni-mobile-container")
              .classList.add("tw-hidden");
          } else {
            primaryNavContainer.classList.remove(classToToggle);
          }
        }
      }
    });
  };

  const mobileMenuObserver = new MutationObserver(mutationHandler);
  mobileMenuObserver.observe(menuBurger, { attributes: true });
};
