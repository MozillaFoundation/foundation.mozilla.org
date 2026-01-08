/**
 * Css selectors for primary navigation elements.
 */
const SELECTORS = {
  primaryNav: ".primary-nav-ns",
  primaryNavGrid: ".primary-nav-ns__grid",
  hamburger: ".primary-nav-ns .hamburger",
  wordmark: ".primary-nav-ns__wordmark",
  menuItem: ".primary-nav-ns__menu-item",
  dropdown: ".primary-nav-ns__dropdown",
  toggle: ".primary-nav-ns__dropdown-toggle",
  kineticTypeWordmark: ".kinetic-type-wordmark",
  searchToggle: ".primary-nav-ns__search-icon .search-toggle",
  searchInputContainer: ".search-input-container",
  searchInput: ".search-input-container input",
};

/**
 * Class names used for toggling state.
 */
const CLASSNAMES = {
  navOpen: "primary-nav-ns-open",
  hidden: "hidden",
  hiddenWordmark: "hidden-wordmark",
  searchOpen: "search-open",
  searchOpenBackdrop: "search-open-backdrop",
  open: "open",
  active: "active",
};

/**
 * Configuration constants for behavior.
 */
const TRANSITION_DURATION = 300;
const DROPDOWN_DELAY = 200;
const DESKTOP_BREAKPOINT = 1024;

/**
 * Initializes the primary navigation component.
 * Sets up mobile and desktop navigation behaviors, including dropdowns and hamburger menu.
 */
export function initPrimaryNav() {
  const hamburger = document.querySelector(SELECTORS.hamburger);
  const nav = document.querySelector(SELECTORS.primaryNav);
  const dropdowns = document.querySelectorAll(SELECTORS.dropdown);

  if (!nav || !hamburger) return;

  // Mobile nav
  hamburger.addEventListener("click", () => {
    nav.classList.toggle(CLASSNAMES.open);
    hamburger.classList.toggle(CLASSNAMES.active);

    if (nav.classList.contains(CLASSNAMES.open)) {
      document.body.classList.add(CLASSNAMES.navOpen);
    } else {
      setTimeout(() => {
        document.body.classList.remove(CLASSNAMES.navOpen);
      }, TRANSITION_DURATION); // Allow time for transition
    }

    // If search input is open, close it when opening mobile nav
    const searchInputContainer = document.querySelector(
      SELECTORS.searchInputContainer,
    );
    const searchToggle = document.querySelector(SELECTORS.searchToggle);
    if (
      nav.classList.contains(CLASSNAMES.open) &&
      searchInputContainer.classList.contains(CLASSNAMES.searchOpen)
    ) {
      searchInputContainer.classList.remove(CLASSNAMES.searchOpen);
      searchToggle.classList.remove(CLASSNAMES.searchOpen);
      searchInputContainer.style.maxHeight = null;
      searchInputContainer.setAttribute("aria-expanded", "false");
    }
  });

  // Dropdown control helpers
  function openDropdown(menu, dropdown, toggle) {
    if (menu.classList.contains("open")) return;
    menu.classList.add("open");
    dropdown.style.maxHeight = dropdown.scrollHeight + "px";
    dropdown.setAttribute("aria-hidden", "false");
    dropdown.removeAttribute("inert");
    toggle.setAttribute("aria-expanded", "true");
  }

  function closeDropdown(menu, dropdown, toggle) {
    if (!menu.classList.contains("open")) return;
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

    // Assign a pseudo random id to the dropdown in order to link it with the toggle via aria-controls.
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
      if (window.innerWidth < DESKTOP_BREAKPOINT) return;
      clearTimeout(hideTimeout);
      showTimeout = setTimeout(() => {
        openDropdown(menu, dropdown, toggle);
      }, DROPDOWN_DELAY);
    });

    menu.addEventListener("mouseleave", () => {
      if (window.innerWidth < DESKTOP_BREAKPOINT) return;
      clearTimeout(showTimeout);
      hideTimeout = setTimeout(() => {
        closeDropdown(menu, dropdown, toggle);
      }, DROPDOWN_DELAY);
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
  const nav = document.querySelector(SELECTORS.primaryNav);
  const grid = document.querySelector(SELECTORS.primaryNavGrid);
  const wordmark = document.querySelector(SELECTORS.wordmark);
  const kineticTypeWordmark = document.querySelector(
    SELECTORS.kineticTypeWordmark,
  );

  if (!nav || !grid || !wordmark) return;

  // If kineticTypeWordmark is not present, always show the wordmark
  if (!kineticTypeWordmark) {
    wordmark.classList.remove(CLASSNAMES.hidden);
    grid.classList.remove(CLASSNAMES.hiddenWordmark);
    return;
  }

  const navHeight = nav.offsetHeight;

  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        wordmark.classList.add(CLASSNAMES.hidden);
        grid.classList.add(CLASSNAMES.hiddenWordmark);
      } else {
        wordmark.classList.remove(CLASSNAMES.hidden);
        grid.classList.remove(CLASSNAMES.hiddenWordmark);
      }
    },
    {
      root: null, // viewport
      rootMargin: `-${navHeight}px  0px 0px 0px`,
      threshold: 0.01, // as soon as even 1% is visible/invisible
    },
  );

  observer.observe(kineticTypeWordmark);
}

/**
 * Initializes the search input toggle functionality, toggling visibility on search icon click.
 */
export function initSearchToggle() {
  const searchToggle = document.querySelector(SELECTORS.searchToggle);
  const searchInputContainer = document.querySelector(
    SELECTORS.searchInputContainer,
  );
  const searchInput = document.querySelector(SELECTORS.searchInput);
  const primaryNav = document.querySelector(SELECTORS.primaryNav);
  const hamburger = document.querySelector(SELECTORS.hamburger);

  if (!searchToggle || !searchInputContainer || !searchInput) return;

  // Create backdrop element
  const backdrop = document.createElement("div");
  backdrop.classList.add(CLASSNAMES.searchOpenBackdrop);
  searchInputContainer.parentNode.insertBefore(backdrop, searchInputContainer);

  function toggleSearchInputVisibility() {
    if (searchInputContainer.classList.contains(CLASSNAMES.searchOpen)) {
      searchToggle.classList.remove(CLASSNAMES.searchOpen);
      searchInputContainer.classList.remove(CLASSNAMES.searchOpen);
      searchInputContainer.style.maxHeight = null;
      searchInputContainer.setAttribute("aria-expanded", "false");
      return;
    }

    // If mobile navigation is open, close it before opening search drawer
    if (primaryNav.classList.contains(CLASSNAMES.open)) {
      primaryNav.classList.remove(CLASSNAMES.open);
      hamburger.classList.remove(CLASSNAMES.active);
      setTimeout(() => {
        document.body.classList.remove(CLASSNAMES.navOpen);
      }, TRANSITION_DURATION); // Allow time for transition
    }

    searchToggle.classList.add(CLASSNAMES.searchOpen);
    searchInputContainer.classList.add(CLASSNAMES.searchOpen);
    searchInputContainer.style.maxHeight =
      searchInputContainer.scrollHeight + "px";
    searchInputContainer.setAttribute("aria-expanded", "true");
    searchInput.focus({ preventScroll: true });
  }

  searchToggle.addEventListener("click", (e) => {
    e.preventDefault();
    toggleSearchInputVisibility();
  });

  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      e.preventDefault();
      toggleSearchInputVisibility();
      searchToggle.focus({ preventScroll: true });
    }
  });

  backdrop.addEventListener("click", () => {
    toggleSearchInputVisibility();
    searchToggle.focus({ preventScroll: true });
  });

  document.body.addEventListener("keydown", (e) => {
    if (
      e.key === "Escape" &&
      searchInputContainer.classList.contains(CLASSNAMES.searchOpen)
    ) {
      e.preventDefault();
      toggleSearchInputVisibility();
      searchToggle.focus({ preventScroll: true });
    }
  });
}
