const SELECTORS = {
  primaryNav: ".primary-nav",
  hamburger: ".primary-nav .hamburger",
  menuItem: ".primary-nav__menu-item",
  dropdown: ".primary-nav__dropdown",
  toggle: ".primary-nav__dropdown-toggle",
};

export function initPrimaryNav() {
  console.log("Initializing primary navigation...");

  const hamburger = document.querySelector(SELECTORS.hamburger);
  const nav = document.querySelector(SELECTORS.primaryNav);
  const dropdowns = document.querySelectorAll(SELECTORS.dropdown);

  if (!nav || !hamburger) return;

  document.body.classList.add("has-primary-nav");

  // Mobile nav
  hamburger.addEventListener("click", () => {
    nav.classList.toggle("open");
    hamburger.classList.toggle("active");
  });

  // Menu dropdowns
  dropdowns.forEach((dropdown) => {
    const toggle = document.createElement("div");
    const menu = dropdown.parentElement;

    // Mobile toggle
    toggle.classList.add(SELECTORS.toggle.replace(".", ""));
    toggle.addEventListener("click", (event) => {
      if (window.innerWidth >= 1024) {
        return;
      }
      const openMenus = document.querySelectorAll(`${SELECTORS.menuItem}.open`);
      openMenus.forEach((openMenu) => {
        if (openMenu === menu) return;
        openMenu.classList.remove("open");
        openMenu.querySelector(SELECTORS.dropdown).style.maxHeight = null;
      });

      if (menu.classList.contains("open")) {
        menu.classList.remove("open");
        dropdown.style.maxHeight = null;
      } else {
        menu.classList.add("open");
        dropdown.style.maxHeight = dropdown.scrollHeight + "px";
      }
    });

    menu.insertBefore(toggle, dropdown);

    // Desktop nav mouse enter/leave events
    menu.addEventListener("mouseenter", () => {
      if (window.innerWidth < 1024) {
        return;
      }
      menu.classList.add("open");
      dropdown.style.maxHeight = dropdown.scrollHeight + "px";
    });
    menu.addEventListener("mouseleave", () => {
      if (window.innerWidth < 1024) {
        return;
      }
      menu.classList.remove("open");
      dropdown.style.maxHeight = null;
    });
  });
}
