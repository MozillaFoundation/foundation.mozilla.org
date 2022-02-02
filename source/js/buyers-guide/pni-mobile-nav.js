/**
 * Adding a click event listener for the mobile navigation on PNI.
 * If the navigation menu button is clicked, open the navigation panel.
 */

const PNIMobileNav = {
  init: () => {
    const mobileNav = document.querySelector("#pni-nav-mobile");

    mobileNav.addEventListener("click", (e) => {
      mobileNav
        .querySelector(".dropdown-nav")
        .classList.toggle("dropdown-nav-open");
    });
  },
};

export default PNIMobileNav;
