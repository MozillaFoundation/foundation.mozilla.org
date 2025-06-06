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
 * Helpers.
 */
function throttle(fn, limit) {
  let lastCall = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      fn.apply(this, args);
    }
  };
}

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

    // Desktop nav mouse enter/leave events with debounce
    let showTimeout, hideTimeout;

    menu.addEventListener("mouseenter", () => {
      if (window.innerWidth < 1024) return;
      clearTimeout(hideTimeout);
      showTimeout = setTimeout(() => {
        menu.classList.add("open");
        dropdown.style.maxHeight = dropdown.scrollHeight + "px";
      }, 200);
    });

    menu.addEventListener("mouseleave", () => {
      if (window.innerWidth < 1024) return;
      clearTimeout(showTimeout);
      hideTimeout = setTimeout(() => {
        menu.classList.remove("open");
        dropdown.style.maxHeight = null;
      }, 200);
    });
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

  // Pages with no kineticTypeWordmark should always show the navigation wordmark
  if (!kineticTypeWordmark) {
    wordmark.classList.remove("hidden");
    grid.classList.remove("hidden-wordmark");
    return;
  }

  // Detect if kineticTypeWordmark is visible on viewport
  const isVisible = () => {
    const rect = kineticTypeWordmark.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <=
        (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  };

  // Initial check
  if (isVisible()) {
    wordmark.classList.add("hidden");
    grid.classList.add("hidden-wordmark");
  } else {
    wordmark.classList.remove("hidden");
    grid.classList.remove("hidden-wordmark");
  }

  // Scroll event listener with throttle
  window.addEventListener(
    "scroll",
    throttle(() => {
      if (isVisible()) {
        wordmark.classList.add("hidden");
        grid.classList.add("hidden-wordmark");
      } else {
        wordmark.classList.remove("hidden");
        grid.classList.remove("hidden-wordmark");
      }
    }, 200),
  );
}
