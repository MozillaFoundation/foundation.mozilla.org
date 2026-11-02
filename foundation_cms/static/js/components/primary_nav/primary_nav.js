import { CLASSNAMES, EVENTS, MOBILE_MEDIA_QUERY, SELECTORS } from "./config.js";
import { initDisclosures } from "./disclosures.js";
import { NavDrawerController } from "./drawer.js";
import { NavPanelsController } from "./panels.js";

/**
 * Initializes the primary navigation: LP's Nav, with desktop section panels
 * and a phone drawer of section rows.
 */
export function initPrimaryNav() {
  const navEl = document.querySelector(SELECTORS.primaryNav);
  if (!navEl) return;

  const panels = new NavPanelsController(navEl);
  const drawer = new NavDrawerController(navEl);

  const closeMenus = () => {
    panels.close();
    drawer.close();
  };

  panels.triggerEls.forEach((triggerEl) => {
    triggerEl.addEventListener("click", () => {
      panels.toggle(triggerEl.dataset.navPanel);
    });
  });

  drawer.menuButtonEl?.addEventListener("click", () => {
    drawer.toggle();
  });

  if (drawer.drawerEl) initDisclosures(drawer.drawerEl);

  // Search measures the header as it opens, so the drawer goes at once.
  document.addEventListener(EVENTS.searchWillOpen, () => {
    panels.close();
    drawer.close({ immediate: true });
  });

  // Lets other overlays, such as gallery modals, dismiss the nav menus.
  document.addEventListener(EVENTS.closeMenus, closeMenus);

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;

    if (drawer.isOpen()) {
      drawer.close({ returnFocus: true });
    } else if (panels.isOpen()) {
      panels.close({ returnFocus: true });
    }
  });

  document.addEventListener("click", (event) => {
    if (navEl.contains(event.target)) return;
    closeMenus();
  });

  // The panels and the drawer each exist on one side of the mobile boundary.
  window.matchMedia?.(MOBILE_MEDIA_QUERY)?.addEventListener("change", () => {
    panels.close();
    drawer.close({ immediate: true });
  });
}

/**
 * Initializes the visibility of the nav logo based on scroll position.
 * Hides the logo while the homepage's kinetic type wordmark is visible in the
 * viewport, so the name is not shown twice.
 */
export function initWordmarkVisibilityOnScroll() {
  const navEl = document.querySelector(SELECTORS.primaryNav);
  const kineticTypeWordmark = document.querySelector(
    SELECTORS.kineticTypeWordmark,
  );

  if (!navEl || !kineticTypeWordmark) return;

  const observer = new IntersectionObserver(
    ([entry]) => {
      navEl.classList.toggle(CLASSNAMES.logoHidden, entry.isIntersecting);
    },
    {
      root: null, // viewport
      rootMargin: `-${navEl.offsetHeight}px 0px 0px 0px`,
      threshold: 0.01, // as soon as even 1% is visible/invisible
    },
  );

  observer.observe(kineticTypeWordmark);
}
