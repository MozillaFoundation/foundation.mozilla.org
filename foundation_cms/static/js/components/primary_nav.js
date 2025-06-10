/**
 * Css selectors for primary navigation elements.
 */
const SELECTORS = {
  primaryNav: ".primary-nav",
  primaryNavGrid: ".primary-nav__grid",
  hamburger: ".primary-nav .hamburger",
  wordmark: ".primary-nav__wordmark",
  menuItem: ".primary-nav__menu-item",
  dropdown: ".primary-nav__dropdown",
  toggle: ".primary-nav__dropdown-toggle",
  kineticTypeWordmark: ".kinetic-type-wordmark",
};

/**
 * Initializes the primary navigation component.
 * Sets up mobile and desktop navigation behaviors, including dropdowns and hamburger menu.
 */
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

  // Dropdown control helpers
  function openDropdown(menu, dropdown, toggle) {
    menu.classList.add("open");
    dropdown.style.maxHeight = dropdown.scrollHeight + "px";
    dropdown.setAttribute("aria-hidden", "false");
    dropdown.removeAttribute("inert");
    toggle.setAttribute("aria-expanded", "true");
  }

  function closeDropdown(menu, dropdown, toggle) {
    menu.classList.remove("open");
    dropdown.style.maxHeight = null;
    dropdown.setAttribute("aria-hidden", "true");
    dropdown.setAttribute("inert", "");
    toggle.setAttribute("aria-expanded", "false");
  }

  function closeAllOtherDropdowns(currentMenu) {
    document
      .querySelectorAll(`${SELECTORS.menuItem}.open`)
      .forEach((openMenu) => {
        if (openMenu === currentMenu) return;
        const openDropdown = openMenu.querySelector(SELECTORS.dropdown);
        const openToggle = openMenu.querySelector(SELECTORS.toggle);
        if (openDropdown && openToggle) {
          closeDropdown(openMenu, openDropdown, openToggle);
        }
      });
  }

  // Menu dropdowns
  dropdowns.forEach((dropdown) => {
    const toggle = document.createElement("div");
    const menu = dropdown.parentElement;
    const anchor = menu.querySelector("a");

    const dropdownId =
      dropdown.id || `dropdown-${Math.random().toString(36).slice(2, 8)}`;
    dropdown.id = dropdownId;

    // Mobile toggle
    toggle.classList.add(SELECTORS.toggle.replace(".", ""));

    toggle.setAttribute("role", "button");
    toggle.setAttribute("tabindex", "0");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", dropdownId);
    dropdown.setAttribute("aria-hidden", "true");
    dropdown.setAttribute("inert", "");

    anchor.insertAdjacentElement("afterend", toggle);

    toggle.addEventListener("click", () => {
      if (window.innerWidth >= 1024) return;

      const isOpen = menu.classList.contains("open");

      if (isOpen) {
        closeDropdown(menu, dropdown, toggle);
      } else {
        closeAllOtherDropdowns(menu);
        openDropdown(menu, dropdown, toggle);
      }
    });

    toggle.addEventListener("keydown", (e) => {
      if (e.key !== "Enter" && e.key !== " ") return;
      e.preventDefault();
      const isOpen = menu.classList.contains("open");

      if (isOpen) {
        closeDropdown(menu, dropdown, toggle);
      } else {
        closeAllOtherDropdowns(menu);
        openDropdown(menu, dropdown, toggle);
      }
    });

    // Desktop nav mouse enter/leave events with debounce
    let showTimeout, hideTimeout;

    menu.addEventListener("mouseenter", () => {
      if (window.innerWidth < 1024) return;
      clearTimeout(hideTimeout);
      showTimeout = setTimeout(() => {
        openDropdown(menu, dropdown, toggle);
      }, 200);
    });

    menu.addEventListener("mouseleave", () => {
      if (window.innerWidth < 1024) return;
      clearTimeout(showTimeout);
      hideTimeout = setTimeout(() => {
        closeDropdown(menu, dropdown, toggle);
      }, 200);
    });
  });

  // Esc key closes all menus
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeAllOtherDropdowns(null);
    }
  });
}

/**
 * Initializes the visibility of the wordmark based on scroll position.
 * Hides the navigation wordmark when the kinetic type wordmark is visible in the viewport.
 */
export function initWordmarkVisibilityOnScroll() {
  const grid = document.querySelector(SELECTORS.primaryNavGrid);
  const wordmark = document.querySelector(SELECTORS.wordmark);
  const kineticTypeWordmark = document.querySelector(
    SELECTORS.kineticTypeWordmark,
  );

  if (!grid || !wordmark) return;

  // If kineticTypeWordmark is not present, always show the wordmark
  if (!kineticTypeWordmark) {
    wordmark.classList.remove("hidden");
    grid.classList.remove("hidden-wordmark");
    return;
  }

  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        wordmark.classList.add("hidden");
        grid.classList.add("hidden-wordmark");
      } else {
        wordmark.classList.remove("hidden");
        grid.classList.remove("hidden-wordmark");
      }
    },
    {
      root: null, // viewport
      threshold: 0.01, // as soon as even 1% is visible/invisible
    },
  );

  observer.observe(kineticTypeWordmark);
}
