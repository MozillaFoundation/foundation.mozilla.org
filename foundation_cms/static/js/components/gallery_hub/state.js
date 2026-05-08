export const GALLERY_HUB_STATE_CHANGE = "galleryHub:stateChange";

const DEFAULT_STATE = {
  activeIndex: 0,
  activeFilters: {},
  filteredProjectIds: [],
  modalOpen: null,
  totalProjects: 0,
  viewMode: "intro",
};

let state = { ...DEFAULT_STATE };

export function getGalleryHubState() {
  return {
    ...state,
    activeFilters: { ...state.activeFilters },
    filteredProjectIds: [...state.filteredProjectIds],
  };
}

export function setGalleryHubState(patch) {
  state = {
    ...state,
    ...patch,
    activeFilters: patch.activeFilters
      ? { ...patch.activeFilters }
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

export function subscribeGalleryHubState(callback) {
  const handler = (event) => callback(event.detail);

  document.addEventListener(GALLERY_HUB_STATE_CHANGE, handler);

  return () => {
    document.removeEventListener(GALLERY_HUB_STATE_CHANGE, handler);
  };
}
