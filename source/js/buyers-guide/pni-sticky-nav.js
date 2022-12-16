const PNIStickyNav = {
  init: () => {
    const navContainer = document.querySelector(".primary-nav-container");

    if (!navContainer) return;

    let lastScroll = 0;
    window.addEventListener("scroll", () => {
      let currentScroll = window.pageYOffset;
      if (currentScroll - lastScroll > 0 && currentScroll >= 300) {
        navContainer.classList.add("tw-h-0", "tw-overflow-hidden");
      } else {
        // scrolled up -- header
        navContainer.classList.remove("tw-h-0");
      }
      lastScroll = currentScroll;
    });
  },
};

export default PNIStickyNav;
