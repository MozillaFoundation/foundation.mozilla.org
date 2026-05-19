/**
 * Tiny shared state store for Gallery Hub modules.
 *
 * The vertical carousel, modal overlays, and follow-up filter/list tickets all
 * read and write the same state. This module keeps updates centralized and
 * broadcasts changes through a document-level custom event.
 *
 * @module galleryHubState
 */

export const GALLERY_HUB_STATE_CHANGE = "galleryHub:stateChange";

/**
 * @typedef {Object} GalleryHubState
 * @property {number} activeIndex - Index within the filtered project list.
 * @property {Object<string, *>} activeFilters - Filter state owned by follow-up tickets.
 * @property {string[]} filteredProjectIds - Project ids visible after filtering.
 * @property {?string} modalOpen - Open modal id, or null when overlays are closed.
 * @property {number} totalProjects - Total number of projects rendered on the page.
 * @property {string} viewMode - Current gallery view mode.
 */

const DEFAULT_STATE = {
  activeIndex: 0,
  activeFilters: {},
  filteredProjectIds: [],
  modalOpen: null,
  totalProjects: 0,
  viewMode: "intro",
};

let state = { ...DEFAULT_STATE };

/**
 * Clone filter state so array values are never shared between modules.
 *
 * @param {Object<string, *>} filters - Filter state to clone.
 * @returns {Object<string, *>}
 */
function cloneFilters(filters) {
  return Object.fromEntries(
    Object.entries(filters).map(([key, value]) => [
      key,
      Array.isArray(value) ? [...value] : value,
    ]),
  );
}

/**
 * Get a cloned snapshot of the current Gallery Hub state.
 *
 * @returns {GalleryHubState}
 */
export function getGalleryHubState() {
  return {
    ...state,
    activeFilters: cloneFilters(state.activeFilters),
    filteredProjectIds: [...state.filteredProjectIds],
  };
}

/**
 * Merge a partial patch into Gallery Hub state and notify subscribers.
 *
 * @param {Partial<GalleryHubState>} patch - State fields to update.
 */
export function setGalleryHubState(patch) {
  state = {
    ...state,
    ...patch,
    activeFilters: patch.activeFilters
      ? cloneFilters(patch.activeFilters)
      : state.activeFilters,
    filteredProjectIds: patch.filteredProjectIds
      ? [...patch.filteredProjectIds]
      : state.filteredProjectIds,
  };

  document.dispatchEvent(
    new CustomEvent(GALLERY_HUB_STATE_CHANGE, {
      detail: getGalleryHubState(),
    }),
  );
}

/**
 * Subscribe to Gallery Hub state updates.
 *
 * @param {(state: GalleryHubState) => void} callback - Called after each state patch.
 * @returns {() => void} Unsubscribe function.
 */
export function subscribeGalleryHubState(callback) {
  const handler = (event) => callback(event.detail);

  document.addEventListener(GALLERY_HUB_STATE_CHANGE, handler);

  return () => {
    document.removeEventListener(GALLERY_HUB_STATE_CHANGE, handler);
  };
}
