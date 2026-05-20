/**
 * Modal overlay controller for the Gallery Hub project list and filter panel.
 *
 * This module intentionally only owns modal visibility and modal trigger
 * accessibility state. Project carousel navigation lives in project_carousel.js.
 *
 * @module galleryHubOverlay
 */

import { GALLERY_HUB_CLASSES, GALLERY_HUB_SELECTORS } from "./config";
import {
  getGalleryHubState,
  setGalleryHubState,
  subscribeGalleryHubState,
} from "./state";

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

    modal.hidden = !isOpen;
  });

  toggles.forEach((toggle) => {
    const isOpen = toggle.dataset.galleryHubModalToggle === modalOpen;

    toggle.setAttribute("aria-expanded", `${isOpen}`);
  });
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

  subscribeGalleryHubState((state) => {
    syncModal(root, modalLayer, modals, toggles, state.modalOpen);
  });

  syncModal(root, modalLayer, modals, toggles, getGalleryHubState().modalOpen);

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const state = getGalleryHubState();
      const modal = toggle.dataset.galleryHubModalToggle;

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

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    if (!getGalleryHubState().modalOpen) return;

    setGalleryHubState({ modalOpen: null });
  });
}
