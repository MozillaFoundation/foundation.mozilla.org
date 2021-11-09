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
