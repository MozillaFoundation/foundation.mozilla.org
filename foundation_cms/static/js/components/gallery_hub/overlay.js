/**
 * Modal overlay controller for the Gallery Hub project list and filter panel.
 *
 * This module intentionally only owns modal visibility and modal trigger
 * accessibility state. Project carousel navigation lives in project_carousel.js.
 *
 * @module galleryHubOverlay
 */

import {
  GALLERY_HUB_CLASSES,
  GALLERY_HUB_MODAL_IDS,
  GALLERY_HUB_SELECTORS,
  GALLERY_HUB_VIEW_MODES,
} from "./config";
import {
  CLASSNAMES as PRIMARY_NAV_CLASSNAMES,
  EVENTS as PRIMARY_NAV_EVENTS,
  SELECTORS as PRIMARY_NAV_SELECTORS,
} from "../primary_nav/config.js";
import {
  getGalleryHubState,
  setGalleryHubState,
  subscribeGalleryHubState,
} from "./state";

const FOCUSABLE_SELECTOR = [
  "a[href]",
  "button:not([disabled])",
  "input:not([disabled])",
  "select:not([disabled])",
  "textarea:not([disabled])",
  "[tabindex]:not([tabindex='-1'])",
].join(",");

const ANIMATED_MODAL_IDS = new Set(Object.values(GALLERY_HUB_MODAL_IDS));
const MODAL_CLOSE_FALLBACK_MS = 360;
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)",
);
const modalCloseTimers = new WeakMap();

let lastFocusedElement = null;

/**
 * Close primary-nav dropdowns that may otherwise layer above gallery modals.
 */
function closePrimaryNavDropdowns() {
  document
    .querySelectorAll(
      `${PRIMARY_NAV_SELECTORS.menuItem}.${PRIMARY_NAV_CLASSNAMES.open}`,
    )
    .forEach((menu) => {
      const dropdown = menu.querySelector(PRIMARY_NAV_SELECTORS.dropdown);
      const toggle = menu.querySelector(PRIMARY_NAV_SELECTORS.toggle);

      menu.classList.remove(PRIMARY_NAV_CLASSNAMES.open);

      if (dropdown) {
        dropdown.style.maxHeight = null;
        dropdown.setAttribute("aria-hidden", "true");
        dropdown.setAttribute("inert", "");
      }

      toggle?.setAttribute("aria-expanded", "false");
    });
}

/**
 * Close global nav/search UI before opening a gallery modal.
 */
function closePrimaryNavOverlays() {
  closePrimaryNavDropdowns();
  document.dispatchEvent(
    new CustomEvent(PRIMARY_NAV_EVENTS.primaryNavWillOpen),
  );
}

/**
 * Return whether a modal should use the animation lifecycle.
 *
 * @param {HTMLElement} modal - Modal panel element.
 * @returns {boolean} Whether modal open/close should animate.
 */
function isAnimatedModal(modal) {
  return ANIMATED_MODAL_IDS.has(modal.dataset.galleryHubModal);
}

/**
 * Cancel any pending delayed hide for a modal.
 *
 * @param {HTMLElement} modal - Modal panel element.
 */
function cancelModalCloseTimer(modal) {
  const timer = modalCloseTimers.get(modal);

  if (!timer) return;

  window.clearTimeout(timer);
  modalCloseTimers.delete(modal);
}

/**
 * Return the element whose exit animation controls delayed hiding.
 *
 * @param {HTMLElement} modal - Modal panel element.
 * @returns {?HTMLElement} Element expected to emit the final animationend.
 */
function getModalAnimationTarget(modal) {
  if (modal.dataset.galleryHubModal === GALLERY_HUB_MODAL_IDS.projectList) {
    return modal.querySelector(".gallery-hub-modal__body");
  }

  return modal.querySelector(".gallery-hub-modal__panel");
}

/**
 * Hide a modal after its closing animation completes.
 *
 * @param {HTMLElement} modal - Modal panel element.
 * @param {?HTMLElement} modalLayer - Element that wraps modal panels.
 */
function hideModalAfterAnimation(modal, modalLayer) {
  const animationTarget = getModalAnimationTarget(modal);

  if (!animationTarget || prefersReducedMotion.matches) {
    modal.hidden = true;
    modal.classList.remove(GALLERY_HUB_CLASSES.modalClosing);
    if (modalLayer) modalLayer.hidden = true;
    return;
  }

  const finish = () => {
    cancelModalCloseTimer(modal);
    animationTarget.removeEventListener("animationend", onAnimationEnd);
    modal.hidden = true;
    modal.classList.remove(GALLERY_HUB_CLASSES.modalClosing);

    if (
      modalLayer &&
      !modalLayer.querySelector(`${GALLERY_HUB_SELECTORS.modal}:not([hidden])`)
    ) {
      modalLayer.hidden = true;
    }
  };
  const timer = window.setTimeout(finish, MODAL_CLOSE_FALLBACK_MS);

  modalCloseTimers.set(modal, timer);

  const onAnimationEnd = (event) => {
    if (event.target !== animationTarget) return;

    finish();
  };

  animationTarget.addEventListener("animationend", onAnimationEnd);
}

/**
 * Return the currently open modal panel.
 *
 * @param {HTMLElement[]} modals - Modal panel elements.
 * @param {?string} modalOpen - Currently open modal id.
 * @returns {?HTMLElement} Open modal element, if any.
 */
function getOpenModal(modals, modalOpen) {
  return (
    modals.find((modal) => modal.dataset.galleryHubModal === modalOpen) || null
  );
}

/**
 * Return focusable controls in a modal, skipping hidden list rows.
 *
 * @param {HTMLElement} modal - Modal panel element.
 * @returns {HTMLElement[]} Focusable controls.
 */
function getFocusableElements(modal) {
  return Array.from(modal.querySelectorAll(FOCUSABLE_SELECTOR)).filter(
    (element) => !element.closest("[hidden]"),
  );
}

/**
 * Reflect the current modal id onto the overlay layer, modal panels, and
 * trigger aria attributes.
 *
 * @param {HTMLElement} root - Gallery Hub root element.
 * @param {?HTMLElement} modalLayer - Element that wraps modal panels.
 * @param {HTMLElement[]} modals - Modal panel elements.
 * @param {HTMLElement[]} toggles - Buttons that open modal panels.
 * @param {?string} modalOpen - Currently open modal id.
 */
function syncModal(root, modalLayer, modals, toggles, modalOpen) {
  if (modalLayer) {
    modalLayer.hidden = !modalOpen;
  }

  root.classList.toggle(GALLERY_HUB_CLASSES.modalOpen, Boolean(modalOpen));

  modals.forEach((modal) => {
    const isOpen = modal.dataset.galleryHubModal === modalOpen;
    const shouldAnimate = isAnimatedModal(modal);

    cancelModalCloseTimer(modal);

    if (isOpen) {
      modal.hidden = false;
      modal.classList.remove(GALLERY_HUB_CLASSES.modalClosing);
      return;
    }

    if (shouldAnimate && !modal.hidden) {
      modal.classList.add(GALLERY_HUB_CLASSES.modalClosing);
      if (modalLayer) modalLayer.hidden = false;
      hideModalAfterAnimation(modal, modalLayer);
      return;
    }

    modal.hidden = true;
    modal.classList.remove(GALLERY_HUB_CLASSES.modalClosing);
  });

  toggles.forEach((toggle) => {
    const isOpen = toggle.dataset.galleryHubModalToggle === modalOpen;

    toggle.setAttribute("aria-expanded", `${isOpen}`);
  });
}

/**
 * Keep the project list rows aligned with the filtered carousel state.
 *
 * @param {HTMLElement[]} items - Project list buttons.
 * @param {HTMLElement} root - Gallery Hub root element.
 * @param {Object} state - Current Gallery Hub state snapshot.
 */
function syncProjectList(items, root, state) {
  const visibleProjectIds = new Set(state.filteredProjectIds);
  const activeProjectId = state.filteredProjectIds[state.activeIndex];
  let visibleCount = 0;

  items.forEach((item) => {
    const projectId = item.dataset.projectId;
    const isVisible = visibleProjectIds.has(projectId);
    const isActive = projectId === activeProjectId;
    const itemShell = item.closest(GALLERY_HUB_SELECTORS.projectListItemShell);

    if (itemShell) itemShell.hidden = !isVisible;
    item.setAttribute("aria-current", isActive ? "true" : "false");

    if (isVisible) visibleCount += 1;
  });

  const empty = root.querySelector("[data-gallery-hub-project-list-empty]");

  if (empty) empty.hidden = visibleCount > 0;
}

/**
 * Move focus into a newly opened modal.
 *
 * @param {HTMLElement[]} modals - Modal panel elements.
 * @param {?string} modalOpen - Currently open modal id.
 * @param {Object} state - Current Gallery Hub state snapshot.
 */
function focusOpenModal(modals, modalOpen, state) {
  const modal = getOpenModal(modals, modalOpen);

  if (!modal) return;

  const activeProjectId = state.filteredProjectIds[state.activeIndex];
  const activeItem = modal.querySelector(
    `${GALLERY_HUB_SELECTORS.projectListItem}[data-project-id="${activeProjectId}"]`,
  );
  const focusable = getFocusableElements(modal);

  window.requestAnimationFrame(() => {
    if (activeItem && !activeItem.closest("[hidden]")) {
      activeItem.focus();
      return;
    }

    focusable[0]?.focus();
  });
}

/**
 * Return focus to the modal trigger after the overlay closes.
 */
function restoreTriggerFocus() {
  if (!lastFocusedElement?.isConnected) return;

  lastFocusedElement.focus();
  lastFocusedElement = null;
}

/**
 * Keep Tab key focus inside the active modal.
 *
 * @param {KeyboardEvent} event - Keydown event.
 * @param {HTMLElement[]} modals - Modal panel elements.
 * @param {?string} modalOpen - Currently open modal id.
 */
function trapModalFocus(event, modals, modalOpen) {
  if (event.key !== "Tab") return;

  const modal = getOpenModal(modals, modalOpen);

  if (!modal) return;

  const focusable = getFocusableElements(modal);

  if (!focusable.length) {
    event.preventDefault();
    modal.focus();
    return;
  }

  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
    return;
  }

  if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

/**
 * Initialize Gallery Hub modal overlay controls.
 */
export function initGalleryHubOverlay() {
  const root = document.querySelector(GALLERY_HUB_SELECTORS.root);

  if (!root) return;

  const modalLayer = root.querySelector(GALLERY_HUB_SELECTORS.modalLayer);
  const modals = Array.from(root.querySelectorAll(GALLERY_HUB_SELECTORS.modal));
  const toggles = Array.from(
    root.querySelectorAll(GALLERY_HUB_SELECTORS.modalToggle),
  );
  const projectListItems = Array.from(
    root.querySelectorAll(GALLERY_HUB_SELECTORS.projectListItem),
  );
  let previousModalOpen = getGalleryHubState().modalOpen;

  subscribeGalleryHubState((state) => {
    const modalWasOpen = Boolean(previousModalOpen);
    const modalIsOpen = Boolean(state.modalOpen);

    syncProjectList(projectListItems, root, state);
    syncModal(root, modalLayer, modals, toggles, state.modalOpen);

    if (!modalWasOpen && modalIsOpen) {
      focusOpenModal(modals, state.modalOpen, state);
    }

    if (modalWasOpen && !modalIsOpen) {
      restoreTriggerFocus();
    }

    previousModalOpen = state.modalOpen;
  });

  syncProjectList(projectListItems, root, getGalleryHubState());
  syncModal(root, modalLayer, modals, toggles, getGalleryHubState().modalOpen);

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const state = getGalleryHubState();
      const modal = toggle.dataset.galleryHubModalToggle;

      lastFocusedElement = toggle;

      if (state.modalOpen !== modal) {
        closePrimaryNavOverlays();
      }

      setGalleryHubState({
        modalOpen: state.modalOpen === modal ? null : modal,
      });
    });
  });

  root.querySelectorAll(GALLERY_HUB_SELECTORS.modalClose).forEach((close) => {
    close.addEventListener("click", () => {
      setGalleryHubState({ modalOpen: null });
    });
  });

  [
    PRIMARY_NAV_EVENTS.primaryNavWillOpen,
    PRIMARY_NAV_EVENTS.searchWillOpen,
  ].forEach((eventName) => {
    document.addEventListener(eventName, () => {
      closePrimaryNavDropdowns();

      if (!getGalleryHubState().modalOpen) return;

      setGalleryHubState({ modalOpen: null });
    });
  });

  document.addEventListener("keydown", (event) => {
    const state = getGalleryHubState();

    if (event.key === "Escape" && state.modalOpen) {
      setGalleryHubState({ modalOpen: null });
      return;
    }

    trapModalFocus(event, modals, state.modalOpen);
  });

  projectListItems.forEach((item) => {
    item.addEventListener("click", () => {
      const state = getGalleryHubState();
      const projectIndex = state.filteredProjectIds.indexOf(
        item.dataset.projectId,
      );

      if (projectIndex === -1) return;

      setGalleryHubState({
        activeIndex: projectIndex,
        modalOpen: null,
        viewMode: GALLERY_HUB_VIEW_MODES.project,
      });
    });
  });
}
