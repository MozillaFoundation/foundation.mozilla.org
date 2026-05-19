/**
 * Vertical project carousel controller for the Gallery Hub page.
 *
 * The carousel keeps the Gallery Hub pinned while the user moves from the intro
 * collage into individual projects. It also releases native page scrolling once
 * the user scrolls past the final project so the footer behaves normally.
 *
 * @module galleryHubProjectCarousel
 */

import {
  GALLERY_HUB_CLASSES,
  GALLERY_HUB_INTRO_ENTERING_DURATION,
  GALLERY_HUB_LEGACY_PROJECTS_HASH,
  GALLERY_HUB_SCROLL_COOLDOWN,
  GALLERY_HUB_SCROLL_KEYS,
  GALLERY_HUB_SCROLL_LOCK_CLASS,
  GALLERY_HUB_SCROLL_THRESHOLD,
  GALLERY_HUB_SELECTORS,
  GALLERY_HUB_VIEW_MODES,
  GALLERY_HUB_VIEWPORT_OFFSET_PROPERTY,
  GALLERY_HUB_VIEWPORT_PROPERTY,
} from "./config";
import { isMostlyVerticalGesture, isPastGestureThreshold } from "./gesture";
import {
  getGalleryHubState,
  setGalleryHubState,
  subscribeGalleryHubState,
} from "./state";

let lockedScrollY = 0;

/**
 * Count active filters across scalar and array filter buckets.
 *
 * @param {Object<string, *>} activeFilters - Current filter values.
 * @returns {number} Number of applied filters.
 */
function getActiveFilterCount(activeFilters) {
  return Object.values(activeFilters).reduce((total, value) => {
    if (Array.isArray(value)) return total + value.length;
    return value ? total + 1 : total;
  }, 0);
}

/**
 * Clamp an index to the rendered project range.
 *
 * @param {number} index - Requested index.
 * @param {number} total - Number of available projects.
 * @returns {number} Index constrained to the available range.
 */
function clampIndex(index, total) {
  return Math.max(0, Math.min(index, Math.max(total - 1, 0)));
}

/**
 * Read the Gallery Hub project id from a project element.
 *
 * @param {HTMLElement} project - Project article element.
 * @returns {string|undefined} Project id from the DOM dataset.
 */
function getProjectId(project) {
  return project.dataset.projectId;
}

/**
 * Return project elements whose ids are currently visible after filtering.
 *
 * @param {HTMLElement[]} projects - All rendered project elements.
 * @param {string[]} filteredProjectIds - Project ids allowed by filters.
 * @returns {HTMLElement[]} Visible project elements in DOM order.
 */
function getVisibleProjects(projects, filteredProjectIds) {
  const ids = new Set(filteredProjectIds);

  return projects.filter((project) => ids.has(getProjectId(project)));
}

/**
 * Find the modal toggle whose data value matches the modal that owns a slot.
 *
 * @param {HTMLElement} root - Gallery Hub root element.
 * @param {HTMLElement[]} toggles - Buttons that open modal panels.
 * @param {string} slotSelector - Selector for a modal body slot.
 * @returns {?HTMLElement} Matching toggle, if present.
 */
function getModalToggleForSlot(root, toggles, slotSelector) {
  const modal = root
    .querySelector(slotSelector)
    ?.closest(GALLERY_HUB_SELECTORS.modal);
  const modalId = modal?.dataset.galleryHubModal;

  if (!modalId) return null;

  return (
    toggles.find(
      (toggle) => toggle.dataset.galleryHubModalToggle === modalId,
    ) ?? null
  );
}

/**
 * Toggle root classes for the intro and project states.
 *
 * @param {HTMLElement} root - Gallery Hub root element.
 * @param {string} viewMode - Current view mode.
 */
function syncViewMode(root, viewMode) {
  const isProjectView = viewMode === GALLERY_HUB_VIEW_MODES.project;

  root.classList.toggle(GALLERY_HUB_CLASSES.intro, !isProjectView);
  root.classList.toggle(GALLERY_HUB_CLASSES.projectView, isProjectView);

  if (isProjectView) {
    root.classList.remove(GALLERY_HUB_CLASSES.introEntering);
  }
}

/**
 * Keep the browser scroll position aligned with the JS-controlled gallery.
 */
function keepNavigationInView() {
  if (window.scrollY <= 1) return;

  window.scrollTo({
    top: 0,
    left: 0,
    behavior: "auto",
  });
}

/**
 * Toggle native page scrolling while the Gallery Hub owns vertical navigation.
 *
 * @param {boolean} isLocked - Whether native page scrolling should be locked.
 */
function setPageScrollLock(isLocked) {
  const root = document.documentElement;
  const body = document.body;
  const isCurrentlyLocked = root.classList.contains(
    GALLERY_HUB_SCROLL_LOCK_CLASS,
  );

  if (isLocked === isCurrentlyLocked) return;

  if (isLocked) {
    keepNavigationInView();
    lockedScrollY = window.scrollY;
    body.style.position = "fixed";
    body.style.top = `-${lockedScrollY}px`;
    body.style.left = "0";
    body.style.right = "0";
    body.style.width = "100%";
  }

  root.classList.toggle(GALLERY_HUB_SCROLL_LOCK_CLASS, isLocked);
  body.classList.toggle(GALLERY_HUB_SCROLL_LOCK_CLASS, isLocked);

  if (!isLocked) {
    body.style.removeProperty("position");
    body.style.removeProperty("top");
    body.style.removeProperty("left");
    body.style.removeProperty("right");
    body.style.removeProperty("width");
    window.scrollTo({ top: lockedScrollY, left: 0, behavior: "auto" });
  }
}

/**
 * Check whether the Gallery Hub currently owns document scrolling.
 *
 * @returns {boolean}
 */
function isPageScrollLocked() {
  return document.documentElement.classList.contains(
    GALLERY_HUB_SCROLL_LOCK_CLASS,
  );
}

/**
 * Check whether an input event belongs to a scrollable modal region.
 *
 * @param {Event} event - Browser input event.
 * @returns {boolean}
 */
function isModalScrollTarget(event) {
  return (
    event.target instanceof Element &&
    Boolean(event.target.closest(GALLERY_HUB_SELECTORS.modalScrollable))
  );
}

/**
 * Check whether the Gallery Hub is using the mobile layout.
 *
 * @returns {boolean}
 */
function isMobileLayout() {
  return window.matchMedia("(max-width: 63.9375em)").matches;
}

/**
 * Check whether the user has requested reduced motion.
 *
 * @returns {boolean}
 */
function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/**
 * Mark the active project and hide inactive projects from assistive tech.
 *
 * @param {HTMLElement[]} projects - All rendered project elements.
 * @param {string[]} filteredProjectIds - Project ids allowed by filters.
 * @param {number} activeIndex - Active index within the filtered project list.
 */
function syncProjects(projects, filteredProjectIds, activeIndex) {
  const visibleProjects = getVisibleProjects(projects, filteredProjectIds);
  const activeProject = visibleProjects[activeIndex];

  projects.forEach((project) => {
    const isActive = project === activeProject;
    const visibleIndex = visibleProjects.indexOf(project);
    const position = visibleIndex === -1 ? null : visibleIndex - activeIndex;

    project.classList.toggle(GALLERY_HUB_CLASSES.projectActive, isActive);
    project.setAttribute("aria-hidden", String(!isActive));

    if (position !== null && Math.abs(position) <= 2) {
      project.dataset.galleryHubProjectPosition = String(position);
    } else {
      delete project.dataset.galleryHubProjectPosition;
    }

    if ("inert" in project) {
      project.inert = !isActive;
    }
  });
}

/**
 * Keep the mobile vertical project markers aligned with the filtered projects.
 *
 * @param {HTMLElement[]} markers - Project marker elements.
 * @param {string[]} filteredProjectIds - Project ids allowed by filters.
 * @param {number} activeIndex - Active index within the filtered project list.
 */
function syncProjectMarkers(markers, filteredProjectIds, activeIndex) {
  const ids = new Set(filteredProjectIds);
  const activeProjectId = filteredProjectIds[activeIndex];

  markers.forEach((marker) => {
    const isVisible = ids.has(marker.dataset.projectId);
    const isActive = marker.dataset.projectId === activeProjectId;

    marker.hidden = !isVisible;
    marker.classList.toggle(GALLERY_HUB_CLASSES.projectMarkerActive, isActive);
  });
}

/**
 * Update vertical navigation and modal trigger button labels.
 *
 * @param {Object} controls - Control elements managed by the carousel.
 * @param {?HTMLElement} controls.previous - Previous project button.
 * @param {?HTMLElement} controls.next - Next project button.
 * @param {?HTMLElement} controls.projectListToggle - Project list modal trigger.
 * @param {?HTMLElement} controls.filterToggle - Filter modal trigger.
 * @param {import("./state").GalleryHubState} state - Current Gallery Hub state.
 */
function syncControls(
  { previous, next, projectListToggle, filterToggle },
  state,
) {
  const visibleTotal = state.filteredProjectIds.length;
  const activePosition = visibleTotal ? state.activeIndex + 1 : 0;
  const filterCount = getActiveFilterCount(state.activeFilters);
  const isProjectView = state.viewMode === GALLERY_HUB_VIEW_MODES.project;

  if (previous)
    previous.hidden =
      !isProjectView || visibleTotal <= 1 || state.activeIndex === 0;
  if (next)
    next.hidden =
      !isProjectView ||
      visibleTotal <= 1 ||
      state.activeIndex >= visibleTotal - 1;

  if (projectListToggle) {
    const label = projectListToggle.dataset.galleryHubToggleLabel || "";

    projectListToggle.textContent = `${label} (${activePosition}/${visibleTotal})`;
  }

  if (filterToggle) {
    const label = filterToggle.dataset.galleryHubToggleLabel || "";

    filterToggle.textContent = `${label} (${filterCount})`;
  }
}

/**
 * Initialize intro-to-project transitions and vertical project navigation.
 */
export function initGalleryHubProjectCarousel() {
  const root = document.querySelector(GALLERY_HUB_SELECTORS.root);

  if (!root) return;

  const projects = Array.from(
    root.querySelectorAll(GALLERY_HUB_SELECTORS.project),
  );
  const projectMarkers = Array.from(
    root.querySelectorAll(GALLERY_HUB_SELECTORS.projectMarker),
  );
  const enterButton = root.querySelector(GALLERY_HUB_SELECTORS.enter);
  const previous = root.querySelector(GALLERY_HUB_SELECTORS.previous);
  const next = root.querySelector(GALLERY_HUB_SELECTORS.next);
  const toggles = Array.from(
    root.querySelectorAll(GALLERY_HUB_SELECTORS.modalToggle),
  );
  const projectListToggle = getModalToggleForSlot(
    root,
    toggles,
    GALLERY_HUB_SELECTORS.projectListSlot,
  );
  const filterToggle = getModalToggleForSlot(
    root,
    toggles,
    GALLERY_HUB_SELECTORS.filterSlot,
  );
  const projectIds = projects.map(getProjectId);
  let isReleasedToPageScroll = false;
  let lastScrollAt = 0;
  let touchStartX = null;
  let touchStartY = null;
  let isIntroAnimationComplete = prefersReducedMotion();

  enterButton?.toggleAttribute("disabled", !isIntroAnimationComplete);

  function completeIntroAnimation() {
    isIntroAnimationComplete = true;
    root.classList.remove(GALLERY_HUB_CLASSES.introEntering);
    enterButton?.removeAttribute("disabled");
  }

  if (isIntroAnimationComplete) {
    completeIntroAnimation();
  } else {
    window.setTimeout(
      completeIntroAnimation,
      GALLERY_HUB_INTRO_ENTERING_DURATION,
    );
  }

  const originalScrollRestoration =
    "scrollRestoration" in window.history
      ? window.history.scrollRestoration
      : null;

  if (originalScrollRestoration !== null) {
    window.history.scrollRestoration = "manual";
    window.addEventListener("pagehide", () => {
      window.history.scrollRestoration = originalScrollRestoration;
    });
  }

  if (window.location.hash === GALLERY_HUB_LEGACY_PROJECTS_HASH) {
    window.history.replaceState(
      null,
      "",
      `${window.location.pathname}${window.location.search}`,
    );
    window.scrollTo({ top: 0, behavior: "auto" });
  }

  /**
   * Get the current visual viewport height, falling back to the layout viewport.
   *
   * @returns {number}
   */
  function getViewportHeight() {
    return window.visualViewport?.height ?? window.innerHeight;
  }

  /**
   * Store available viewport height so SCSS can size the gallery stage.
   */
  function updateViewportHeight() {
    const rootTop = Math.max(root.getBoundingClientRect().top, 0);
    const viewportHeight = getViewportHeight() - rootTop;
    const clampedViewportHeight = Math.max(viewportHeight, 320);

    root.style.setProperty(
      GALLERY_HUB_VIEWPORT_PROPERTY,
      `${clampedViewportHeight}px`,
    );
    root.style.setProperty(
      GALLERY_HUB_VIEWPORT_OFFSET_PROPERTY,
      `${rootTop}px`,
    );
    root.classList.toggle(
      GALLERY_HUB_CLASSES.mobileCompact,
      isMobileLayout() && clampedViewportHeight <= 820,
    );
    root.classList.toggle(
      GALLERY_HUB_CLASSES.mobileShort,
      isMobileLayout() && clampedViewportHeight <= 760,
    );
  }

  /**
   * Check whether a downward gesture should leave the Gallery Hub and continue
   * to the page footer.
   *
   * @param {number} delta - Positive for forward/down navigation.
   * @returns {boolean} Whether native page scrolling should resume.
   */
  function shouldReleaseNativeScroll(delta) {
    const state = getGalleryHubState();
    const lastProjectIndex = state.filteredProjectIds.length - 1;

    return (
      state.viewMode === GALLERY_HUB_VIEW_MODES.project &&
      delta > 0 &&
      state.activeIndex >= lastProjectIndex
    );
  }

  /**
   * Unlock the page and nudge the browser into normal document scrolling.
   */
  function releaseToPageScroll() {
    isReleasedToPageScroll = true;
    setPageScrollLock(false);
    window.requestAnimationFrame(() => {
      window.scrollBy({
        top: Math.min(getViewportHeight() * 0.72, root.offsetHeight),
        left: 0,
        behavior: "smooth",
      });
    });
  }

  /**
   * Check whether the Gallery Hub is currently intersecting the viewport.
   *
   * @returns {boolean}
   */
  function isGalleryInScrollRange() {
    const rect = root.getBoundingClientRect();

    return rect.top < getViewportHeight() && rect.bottom > 0;
  }

  /**
   * Move the current Gallery Hub view by one project step.
   *
   * @param {number} delta - Positive for next project, negative for previous.
   */
  function moveProjectBy(delta) {
    const state = getGalleryHubState();

    if (state.modalOpen) return;

    const visibleTotal = state.filteredProjectIds.length;

    if (!visibleTotal) return;

    if (state.viewMode === GALLERY_HUB_VIEW_MODES.intro) {
      if (!isIntroAnimationComplete) return;

      if (delta > 0) {
        setGalleryHubState({
          activeIndex: 0,
          viewMode: GALLERY_HUB_VIEW_MODES.project,
        });
      }

      return;
    }

    if (delta < 0 && state.activeIndex === 0) {
      setGalleryHubState({ viewMode: GALLERY_HUB_VIEW_MODES.intro });
      return;
    }

    setActiveProjectIndex(state.activeIndex + delta);
  }

  /**
   * Set the active project index after clamping it to the current filtered list.
   *
   * @param {number} index - Requested active index.
   */
  function setActiveProjectIndex(index) {
    const state = getGalleryHubState();
    const activeIndex = clampIndex(index, state.filteredProjectIds.length);

    if (activeIndex === state.activeIndex) return;

    setGalleryHubState({ activeIndex });
  }

  /**
   * Check whether a gesture belongs to the carousel transition that just ran.
   *
   * This prevents wheel/touch momentum from landing on the final project and
   * immediately releasing the page to the footer during the same gesture.
   *
   * @returns {boolean}
   */
  function isNavigationCoolingDown() {
    return Date.now() - lastScrollAt < GALLERY_HUB_SCROLL_COOLDOWN;
  }

  /**
   * Keep early gestures from moving the gallery while the first-load intro
   * collage is still animating.
   *
   * @returns {boolean} Whether project navigation should wait.
   */
  function isWaitingForIntroAnimation() {
    const state = getGalleryHubState();

    return (
      state.viewMode === GALLERY_HUB_VIEW_MODES.intro &&
      !isIntroAnimationComplete
    );
  }

  /**
   * Re-pin the Gallery Hub after native page scroll returns to the gallery.
   */
  function restoreGalleryNavigation() {
    if (!isReleasedToPageScroll || window.scrollY > 1) return;

    isReleasedToPageScroll = false;
    setPageScrollLock(true);
    lastScrollAt = Date.now();
  }

  subscribeGalleryHubState((state) => {
    const visibleTotal = state.filteredProjectIds.length;
    const activeIndex = clampIndex(state.activeIndex, visibleTotal);

    // Correct out-of-range indexes after filtering. The follow-up dispatch
    // receives an already-clamped index, so this does not loop indefinitely.
    if (activeIndex !== state.activeIndex) {
      setGalleryHubState({ activeIndex });
      return;
    }

    syncViewMode(root, state.viewMode);
    syncProjects(projects, state.filteredProjectIds, activeIndex);
    syncProjectMarkers(projectMarkers, state.filteredProjectIds, activeIndex);
    syncControls({ previous, next, projectListToggle, filterToggle }, state);

    if (
      !state.modalOpen &&
      !shouldReleaseNativeScroll(1) &&
      isGalleryInScrollRange()
    ) {
      keepNavigationInView();
    }

    if (!isReleasedToPageScroll) {
      setPageScrollLock(true);
    }
  });

  setGalleryHubState({
    activeIndex: 0,
    filteredProjectIds: projectIds,
    totalProjects: projects.length,
    viewMode: GALLERY_HUB_VIEW_MODES.intro,
  });

  updateViewportHeight();
  keepNavigationInView();
  window.requestAnimationFrame(() => {
    updateViewportHeight();
    keepNavigationInView();
  });
  window.addEventListener("resize", updateViewportHeight);
  window.visualViewport?.addEventListener("resize", updateViewportHeight);
  window.visualViewport?.addEventListener("scroll", updateViewportHeight);
  window.addEventListener("scroll", restoreGalleryNavigation, {
    passive: true,
  });

  enterButton?.addEventListener("click", (event) => {
    if (isWaitingForIntroAnimation()) {
      event.preventDefault();
      keepNavigationInView();
      return;
    }

    setGalleryHubState({
      activeIndex: 0,
      viewMode: GALLERY_HUB_VIEW_MODES.project,
    });
  });

  previous?.addEventListener("click", () => {
    const state = getGalleryHubState();

    if (
      state.viewMode === GALLERY_HUB_VIEW_MODES.project &&
      state.activeIndex === 0
    ) {
      setGalleryHubState({ viewMode: GALLERY_HUB_VIEW_MODES.intro });
      return;
    }

    setActiveProjectIndex(state.activeIndex - 1);
  });

  next?.addEventListener("click", () => {
    const state = getGalleryHubState();

    if (state.viewMode === GALLERY_HUB_VIEW_MODES.intro) {
      if (isWaitingForIntroAnimation()) {
        keepNavigationInView();
        return;
      }

      setGalleryHubState({
        activeIndex: 0,
        viewMode: GALLERY_HUB_VIEW_MODES.project,
      });
      return;
    }

    setActiveProjectIndex(state.activeIndex + 1);
  });

  /**
   * Convert wheel gestures into project navigation while the gallery is active.
   *
   * @param {WheelEvent} event - Wheel event captured at the window.
   */
  function handleWheel(event) {
    if (!isGalleryInScrollRange()) return;
    if (Math.abs(event.deltaY) < GALLERY_HUB_SCROLL_THRESHOLD) return;

    if (getGalleryHubState().modalOpen) {
      if (isModalScrollTarget(event)) return;

      event.preventDefault();
      return;
    }

    if (isReleasedToPageScroll) return;

    if (isWaitingForIntroAnimation()) {
      event.preventDefault();
      keepNavigationInView();
      return;
    }

    if (isNavigationCoolingDown()) {
      event.preventDefault();
      return;
    }

    if (shouldReleaseNativeScroll(event.deltaY)) {
      event.preventDefault();
      releaseToPageScroll();
      return;
    }

    lastScrollAt = Date.now();
    event.preventDefault();
    keepNavigationInView();
    moveProjectBy(event.deltaY > 0 ? 1 : -1);
  }

  window.addEventListener("wheel", handleWheel, {
    capture: true,
    passive: false,
  });

  /**
   * Check whether a touch gesture is intended for vertical project navigation.
   *
   * @param {number} deltaX - Horizontal touch movement.
   * @param {number} deltaY - Vertical touch movement.
   * @returns {boolean} Whether the gesture should move projects.
   */
  function isProjectTouchGesture(deltaX, deltaY) {
    return (
      isPastGestureThreshold(deltaX, deltaY, GALLERY_HUB_SCROLL_THRESHOLD) &&
      isMostlyVerticalGesture(deltaX, deltaY)
    );
  }

  root.addEventListener(
    "touchstart",
    (event) => {
      touchStartX = event.touches[0]?.clientX ?? null;
      touchStartY = event.touches[0]?.clientY ?? null;
    },
    { passive: true },
  );

  root.addEventListener(
    "touchmove",
    (event) => {
      if (touchStartX === null || touchStartY === null) return;

      const touchX = event.touches[0]?.clientX ?? touchStartX;
      const touchY = event.touches[0]?.clientY ?? touchStartY;
      const deltaX = touchStartX - touchX;
      const deltaY = touchStartY - touchY;

      if (!isProjectTouchGesture(deltaX, deltaY)) return;
      if (getGalleryHubState().modalOpen) {
        if (isModalScrollTarget(event)) return;

        event.preventDefault();
        return;
      }

      if (isReleasedToPageScroll) return;

      if (isWaitingForIntroAnimation()) {
        event.preventDefault();
        keepNavigationInView();
        return;
      }

      if (isNavigationCoolingDown()) {
        event.preventDefault();
        keepNavigationInView();
        return;
      }

      if (shouldReleaseNativeScroll(deltaY)) {
        releaseToPageScroll();
        return;
      }

      event.preventDefault();
      keepNavigationInView();
    },
    { passive: false },
  );

  root.addEventListener(
    "touchend",
    (event) => {
      if (touchStartX === null || touchStartY === null) return;

      const touchEndX = event.changedTouches[0]?.clientX ?? touchStartX;
      const touchEndY = event.changedTouches[0]?.clientY ?? touchStartY;
      const deltaX = touchStartX - touchEndX;
      const deltaY = touchStartY - touchEndY;

      touchStartX = null;
      touchStartY = null;

      if (!isProjectTouchGesture(deltaX, deltaY)) return;
      if (getGalleryHubState().modalOpen) return;
      if (isReleasedToPageScroll) return;

      if (isWaitingForIntroAnimation()) {
        keepNavigationInView();
        return;
      }

      if (isNavigationCoolingDown()) {
        keepNavigationInView();
        return;
      }

      if (shouldReleaseNativeScroll(deltaY)) {
        releaseToPageScroll();
        return;
      }

      lastScrollAt = Date.now();
      keepNavigationInView();
      moveProjectBy(deltaY > 0 ? 1 : -1);
    },
    { passive: true },
  );

  document.addEventListener("keydown", (event) => {
    if (!GALLERY_HUB_SCROLL_KEYS.has(event.key)) return;

    const delta = event.key.endsWith("Down") ? 1 : -1;

    if (getGalleryHubState().modalOpen) {
      if (isModalScrollTarget(event)) return;

      event.preventDefault();
      return;
    }

    if (isReleasedToPageScroll || !isPageScrollLocked()) return;

    if (isWaitingForIntroAnimation()) {
      event.preventDefault();
      keepNavigationInView();
      return;
    }

    if (isNavigationCoolingDown()) {
      event.preventDefault();
      keepNavigationInView();
      return;
    }

    if (shouldReleaseNativeScroll(delta)) {
      releaseToPageScroll();
      return;
    }

    lastScrollAt = Date.now();
    event.preventDefault();
    keepNavigationInView();
    moveProjectBy(delta);
  });
}
