/**
 * Filter panel controller for Gallery Hub.
 *
 * The panel keeps draft selections local until users display results. Committed
 * filters are written to the shared Gallery Hub state so the carousel and
 * project list stay aligned.
 *
 * @module galleryHubFilterPanel
 */

import { GALLERY_HUB_SELECTORS, GALLERY_HUB_VIEW_MODES } from "./config";
import {
  getGalleryHubState,
  setGalleryHubState,
  subscribeGalleryHubState,
} from "./state";

const FILTER_MODAL_ID = "filter";
const PROJECT_FILTER_DATA_ID = "gallery-hub-project-filter-data";

/**
 * Clone active filter arrays.
 *
 * @param {Object<string, string[]>} filters - Filter state to clone.
 * @returns {Object<string, string[]>}
 */
function cloneFilters(filters) {
  return Object.fromEntries(
    Object.entries(filters).map(([key, values]) => [
      key,
      Array.isArray(values) ? [...values] : values,
    ]),
  );
}

/**
 * Normalize filters by removing empty categories and duplicate values.
 *
 * @param {Object<string, string[]>} filters - Filter state.
 * @param {Set<string>} categories - Supported filter category keys.
 * @returns {Object<string, string[]>}
 */
function normalizeFilters(filters, categories) {
  return Object.fromEntries(
    Object.entries(filters)
      .filter(([category]) => categories.has(category))
      .map(([category, values]) => {
        const valueList = Array.isArray(values) ? values : [values];

        return [category, [...new Set(valueList)].filter(Boolean).sort()];
      })
      .filter(([, values]) => values.length),
  );
}

/**
 * Read per-project filter metadata emitted by the template.
 *
 * @returns {{id: string, filters: Object<string, string[]>}[]}
 */
function getProjectFilterData() {
  const data = document.getElementById(PROJECT_FILTER_DATA_ID);

  if (!data?.textContent) return [];

  try {
    return JSON.parse(data.textContent);
  } catch {
    return [];
  }
}

/**
 * Determine whether a project matches selected filters.
 *
 * Categories are ANDed together. Topic values are ANDed together per design;
 * other category values are ORed.
 *
 * @param {{filters: Object<string, string[]>}} project - Project filter data.
 * @param {Object<string, string[]>} filters - Active filters.
 * @returns {boolean}
 */
function matchesFilters(project, filters) {
  return Object.entries(filters).every(([category, selectedValues]) => {
    const projectValues = new Set(project.filters[category] || []);

    if (category === "topic") {
      return selectedValues.every((value) => projectValues.has(value));
    }

    return selectedValues.some((value) => projectValues.has(value));
  });
}

/**
 * Return project ids visible under the given filters.
 *
 * @param {{id: string, filters: Object<string, string[]>}[]} projects - Filter data.
 * @param {Object<string, string[]>} filters - Active filters.
 * @returns {string[]}
 */
function getFilteredProjectIds(projects, filters) {
  if (!Object.keys(filters).length)
    return projects.map((project) => project.id);

  return projects
    .filter((project) => matchesFilters(project, filters))
    .map((project) => project.id);
}

/**
 * Parse committed filters from the current URL.
 *
 * @param {Set<string>} categories - Supported filter category keys.
 * @returns {Object<string, string[]>}
 */
function getFiltersFromUrl(categories) {
  const params = new URLSearchParams(window.location.search);
  const filters = {};

  categories.forEach((category) => {
    const values = params.getAll(category).filter(Boolean);

    if (values.length) {
      filters[category] = values;
    }
  });

  return normalizeFilters(filters, categories);
}

/**
 * Reflect committed filters into the URL query string.
 *
 * @param {Object<string, string[]>} filters - Active filters.
 * @param {Set<string>} categories - Supported filter category keys.
 */
function syncUrl(filters, categories) {
  const url = new URL(window.location.href);

  categories.forEach((category) => {
    url.searchParams.delete(category);
  });

  categories.forEach((category) => {
    (filters[category] || []).forEach((value) => {
      url.searchParams.append(category, value);
    });
  });

  window.history.replaceState(
    null,
    "",
    `${url.pathname}${url.search}${url.hash}`,
  );
}

/**
 * Initialize Gallery Hub filter panel controls.
 */
export function initGalleryHubFilterPanel() {
  const root = document.querySelector(GALLERY_HUB_SELECTORS.root);

  if (!root) return;

  const panel = root.querySelector(GALLERY_HUB_SELECTORS.filterPanel);

  if (!panel) return;

  const projects = getProjectFilterData();
  const categories = new Set(
    Array.from(root.querySelectorAll(GALLERY_HUB_SELECTORS.filterCategory)).map(
      (category) => category.dataset.galleryHubFilterCategory,
    ),
  );
  const chips = Array.from(
    root.querySelectorAll(GALLERY_HUB_SELECTORS.filterChip),
  );
  const apply = root.querySelector(GALLERY_HUB_SELECTORS.filterApply);
  const reset = root.querySelector(GALLERY_HUB_SELECTORS.filterReset);
  let draftFilters = getFiltersFromUrl(categories);
  let wasFilterOpen = false;

  /**
   * Update chip pressed state and display-results preview count.
   */
  function syncPanel() {
    const previewProjectIds = getFilteredProjectIds(projects, draftFilters);

    chips.forEach((chip) => {
      const values = draftFilters[chip.dataset.filterCategory] || [];
      const isSelected = values.includes(chip.dataset.filterValue);

      chip.setAttribute("aria-pressed", `${isSelected}`);
      chip.classList.toggle("gallery-hub-filter__chip--selected", isSelected);
    });

    if (apply) {
      const count = previewProjectIds.length;
      const label = apply.dataset.galleryHubFilterApplyLabel || "";

      apply.textContent = `${label} (${count})`;
      apply.disabled = count === 0;
    }
  }

  /**
   * Commit filters to shared state and optionally close the panel.
   *
   * @param {Object<string, string[]>} filters - Filters to commit.
   * @param {boolean} shouldClose - Whether to close the modal after commit.
   */
  function commitFilters(filters, shouldClose, shouldEnterProjectView = true) {
    const activeFilters = normalizeFilters(filters, categories);
    const filteredProjectIds = getFilteredProjectIds(projects, activeFilters);
    const patch = {
      activeFilters,
      activeIndex: 0,
      filteredProjectIds,
    };

    if (shouldEnterProjectView) {
      patch.viewMode = GALLERY_HUB_VIEW_MODES.project;
    }

    if (shouldClose) {
      patch.modalOpen = null;
    }

    setGalleryHubState(patch);
    syncUrl(activeFilters, categories);
  }

  root
    .querySelectorAll(GALLERY_HUB_SELECTORS.filterCategoryToggle)
    .forEach((toggle) => {
      toggle.addEventListener("click", () => {
        const category = toggle.closest(GALLERY_HUB_SELECTORS.filterCategory);
        const options = category?.querySelector(
          GALLERY_HUB_SELECTORS.filterOptions,
        );
        const isExpanded = toggle.getAttribute("aria-expanded") === "true";

        toggle.setAttribute("aria-expanded", `${!isExpanded}`);

        if (options) {
          options.hidden = isExpanded;
        }
      });
    });

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const category = chip.dataset.filterCategory;
      const value = chip.dataset.filterValue;
      const values = new Set(draftFilters[category] || []);

      if (values.has(value)) {
        values.delete(value);
      } else {
        values.add(value);
      }

      draftFilters = normalizeFilters(
        {
          ...draftFilters,
          [category]: [...values],
        },
        categories,
      );
      syncPanel();
    });
  });

  reset?.addEventListener("click", () => {
    draftFilters = {};
    syncPanel();
  });

  apply?.addEventListener("click", () => {
    if (apply.disabled) return;

    commitFilters(draftFilters, true);
  });

  subscribeGalleryHubState((state) => {
    const isFilterOpen = state.modalOpen === FILTER_MODAL_ID;

    if (isFilterOpen && !wasFilterOpen) {
      draftFilters = cloneFilters(state.activeFilters);
      syncPanel();
    }

    wasFilterOpen = isFilterOpen;
  });

  if (Object.keys(draftFilters).length) {
    commitFilters(draftFilters, false);
  }

  syncPanel();
}
