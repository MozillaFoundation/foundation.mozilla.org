import {
  getGalleryHubState,
  setGalleryHubState,
  subscribeGalleryHubState,
} from "./state";

const SELECTORS = {
  root: "[data-gallery-hub]",
  enter: "[data-gallery-hub-enter]",
  project: "[data-gallery-hub-project]",
  previous: "[data-gallery-hub-previous]",
  next: "[data-gallery-hub-next]",
  modalLayer: "[data-gallery-hub-modal-layer]",
  modal: "[data-gallery-hub-modal]",
  modalToggle: "[data-gallery-hub-modal-toggle]",
  modalClose: "[data-gallery-hub-modal-close]",
};

const VIEW_MODES = {
  intro: "intro",
  project: "project",
};

const SCROLL_THRESHOLD = 28;
const SCROLL_COOLDOWN = 650;
const GALLERY_VIEWPORT_PROPERTY = "--gallery-hub-viewport-height";
const LEGACY_PROJECTS_HASH = "#gallery-hub-projects";
const SCROLL_KEYS = new Set(["ArrowDown", "ArrowUp", "PageDown", "PageUp"]);
const SCROLL_LOCK_CLASS = "gallery-hub-scroll-locked";

function getActiveFilterCount(activeFilters) {
  return Object.values(activeFilters).reduce((total, value) => {
    if (Array.isArray(value)) return total + value.length;
    return value ? total + 1 : total;
  }, 0);
}

function clampIndex(index, total) {
  return Math.max(0, Math.min(index, Math.max(total - 1, 0)));
}

function getProjectId(project) {
  return project.dataset.projectId;
}

function getVisibleProjects(projects, filteredProjectIds) {
  const ids = new Set(filteredProjectIds);

  return projects.filter((project) => ids.has(getProjectId(project)));
}

function syncViewMode(root, viewMode) {
  const isProjectView = viewMode === VIEW_MODES.project;

  root.classList.toggle("gallery-hub--intro", !isProjectView);
  root.classList.toggle("gallery-hub--project-view", isProjectView);
}

function keepNavigationInView() {
  if (window.scrollY <= 1) return;

  window.scrollTo({
    top: 0,
    left: 0,
    behavior: "auto",
  });
}

function setPageScrollLock(isLocked) {
  document.documentElement.classList.toggle(SCROLL_LOCK_CLASS, isLocked);
  document.body.classList.toggle(SCROLL_LOCK_CLASS, isLocked);
}

function syncProjects(projects, filteredProjectIds, activeIndex) {
  const visibleProjects = getVisibleProjects(projects, filteredProjectIds);
  const activeProject = visibleProjects[activeIndex];

  projects.forEach((project) => {
    const isActive = project === activeProject;

    project.classList.toggle("gallery-hub-project--active", isActive);
    project.setAttribute("aria-hidden", String(!isActive));

    if ("inert" in project) {
      project.inert = !isActive;
    }
  });
}

function syncModal(root, modalLayer, modals, toggles, modalOpen) {
  modalLayer.hidden = !modalOpen;
  root.classList.toggle("gallery-hub--modal-open", Boolean(modalOpen));

  modals.forEach((modal) => {
    const isOpen = modal.dataset.galleryHubModal === modalOpen;

    modal.hidden = !isOpen;
  });

  toggles.forEach((toggle) => {
    const isOpen = toggle.dataset.galleryHubModalToggle === modalOpen;

    toggle.setAttribute("aria-expanded", `${isOpen}`);
  });
}

function syncControls(
  { previous, next, projectListToggle, filterToggle },
  state,
) {
  const visibleTotal = state.filteredProjectIds.length;
  const activePosition = visibleTotal ? state.activeIndex + 1 : 0;
  const filterCount = getActiveFilterCount(state.activeFilters);
  const isProjectView = state.viewMode === VIEW_MODES.project;

  if (previous)
    previous.hidden = !isProjectView || visibleTotal <= 1 || state.activeIndex === 0;
  if (next)
    next.hidden =
      !isProjectView || visibleTotal <= 1 || state.activeIndex >= visibleTotal - 1;

  if (projectListToggle) {
    const label = projectListToggle.dataset.galleryHubToggleLabel || "";

    projectListToggle.textContent = `${label} (${activePosition}/${visibleTotal})`;
  }

  if (filterToggle) {
    const label = filterToggle.dataset.galleryHubToggleLabel || "";

    filterToggle.textContent = `${label} (${filterCount})`;
  }
}

export function initGalleryHubOverlay() {
  const root = document.querySelector(SELECTORS.root);

  if (!root) return;

  const projects = Array.from(root.querySelectorAll(SELECTORS.project));
  const enterButton = root.querySelector(SELECTORS.enter);
  const previous = root.querySelector(SELECTORS.previous);
  const next = root.querySelector(SELECTORS.next);
  const modalLayer = root.querySelector(SELECTORS.modalLayer);
  const modals = Array.from(root.querySelectorAll(SELECTORS.modal));
  const toggles = Array.from(root.querySelectorAll(SELECTORS.modalToggle));
  const projectListToggle = toggles.find(
    (toggle) => toggle.dataset.galleryHubModalToggle === "project-list",
  );
  const filterToggle = toggles.find(
    (toggle) => toggle.dataset.galleryHubModalToggle === "filter",
  );
  const projectIds = projects.map(getProjectId);
  let lastScrollAt = 0;
  let touchStartY = null;

  if ("scrollRestoration" in window.history) {
    window.history.scrollRestoration = "manual";
  }

  if (window.location.hash === LEGACY_PROJECTS_HASH) {
    window.history.replaceState(
      null,
      "",
      `${window.location.pathname}${window.location.search}`,
    );
    window.scrollTo({ top: 0, behavior: "auto" });
  }

  function updateViewportHeight() {
    const rootTop = Math.max(root.getBoundingClientRect().top, 0);
    const viewportHeight = window.innerHeight - rootTop;

    root.style.setProperty(
      GALLERY_VIEWPORT_PROPERTY,
      `${Math.max(viewportHeight, 320)}px`,
    );
  }

  subscribeGalleryHubState((state) => {
    const visibleTotal = state.filteredProjectIds.length;
    const activeIndex = clampIndex(state.activeIndex, visibleTotal);

    if (activeIndex !== state.activeIndex) {
      setGalleryHubState({ activeIndex });
      return;
    }

    syncViewMode(root, state.viewMode);
    syncProjects(projects, state.filteredProjectIds, activeIndex);
    syncModal(root, modalLayer, modals, toggles, state.modalOpen);
    syncControls({ previous, next, projectListToggle, filterToggle }, state);

    if (
      !state.modalOpen &&
      !shouldReleaseNativeScroll(1) &&
      isGalleryInScrollRange()
    ) {
      keepNavigationInView();
    }

    setPageScrollLock(true);
  });

  setGalleryHubState({
    activeIndex: 0,
    filteredProjectIds: projectIds,
    totalProjects: projects.length,
    viewMode: VIEW_MODES.intro,
  });

  updateViewportHeight();
  keepNavigationInView();
  window.requestAnimationFrame(() => {
    updateViewportHeight();
    keepNavigationInView();
  });
  window.addEventListener("resize", updateViewportHeight);

  enterButton?.addEventListener("click", () => {
    setGalleryHubState({
      activeIndex: 0,
      viewMode: VIEW_MODES.project,
    });
  });

  previous?.addEventListener("click", () => {
    const state = getGalleryHubState();

    if (
      state.viewMode === VIEW_MODES.project &&
      state.activeIndex === 0
    ) {
      setGalleryHubState({ viewMode: VIEW_MODES.intro });
      return;
    }

    setGalleryHubState({
      activeIndex: clampIndex(
        state.activeIndex - 1,
        state.filteredProjectIds.length,
      ),
    });
  });

  next?.addEventListener("click", () => {
    const state = getGalleryHubState();

    if (state.viewMode === VIEW_MODES.intro) {
      setGalleryHubState({
        activeIndex: 0,
        viewMode: VIEW_MODES.project,
      });
      return;
    }

    setGalleryHubState({
      activeIndex: clampIndex(
        state.activeIndex + 1,
        state.filteredProjectIds.length,
      ),
    });
  });

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const state = getGalleryHubState();
      const modal = toggle.dataset.galleryHubModalToggle;

      setGalleryHubState({
        modalOpen: state.modalOpen === modal ? null : modal,
      });
    });
  });

  root.querySelectorAll(SELECTORS.modalClose).forEach((close) => {
    close.addEventListener("click", () => {
      setGalleryHubState({ modalOpen: null });
    });
  });

  function moveProjectBy(delta) {
    const state = getGalleryHubState();

    if (state.modalOpen) return;

    const visibleTotal = state.filteredProjectIds.length;

    if (!visibleTotal) return;

    if (state.viewMode === VIEW_MODES.intro) {
      if (delta > 0) {
        setGalleryHubState({
          activeIndex: 0,
          viewMode: VIEW_MODES.project,
        });
      }

      return;
    }

    if (delta < 0 && state.activeIndex === 0) {
      setGalleryHubState({ viewMode: VIEW_MODES.intro });
      return;
    }

    setGalleryHubState({
      activeIndex: clampIndex(state.activeIndex + delta, visibleTotal),
    });
  }

  function shouldReleaseNativeScroll(delta) {
    const state = getGalleryHubState();
    const lastProjectIndex = state.filteredProjectIds.length - 1;

    return (
      state.viewMode === VIEW_MODES.project &&
      delta > 0 &&
      state.activeIndex >= lastProjectIndex
    );
  }

  function releaseToPageScroll() {
    setPageScrollLock(false);
    window.requestAnimationFrame(() => {
      window.scrollBy({
        top: Math.min(window.innerHeight * 0.72, root.offsetHeight),
        left: 0,
        behavior: "smooth",
      });
    });
  }

  function isGalleryInScrollRange() {
    const rect = root.getBoundingClientRect();

    return rect.top < window.innerHeight && rect.bottom > 0;
  }

  function handleWheel(event) {
    if (!isGalleryInScrollRange() && getGalleryHubState().viewMode !== VIEW_MODES.project)
      return;
    if (Math.abs(event.deltaY) < SCROLL_THRESHOLD) return;

    if (shouldReleaseNativeScroll(event.deltaY)) {
      event.preventDefault();
      releaseToPageScroll();
      return;
    }

    const now = Date.now();

    if (now - lastScrollAt < SCROLL_COOLDOWN) {
      event.preventDefault();
      return;
    }

    lastScrollAt = now;
    event.preventDefault();
    keepNavigationInView();
    moveProjectBy(event.deltaY > 0 ? 1 : -1);
  }

  window.addEventListener("wheel", handleWheel, {
    capture: true,
    passive: false,
  });

  root.addEventListener(
    "touchstart",
    (event) => {
      touchStartY = event.touches[0]?.clientY ?? null;
    },
    { passive: true },
  );

  root.addEventListener(
    "touchmove",
    (event) => {
      if (touchStartY === null) return;

      const touchY = event.touches[0]?.clientY ?? touchStartY;
      const deltaY = touchStartY - touchY;

      if (Math.abs(deltaY) < SCROLL_THRESHOLD) return;
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
      if (touchStartY === null) return;

      const touchEndY = event.changedTouches[0]?.clientY ?? touchStartY;
      const deltaY = touchStartY - touchEndY;

      touchStartY = null;

      if (Math.abs(deltaY) < SCROLL_THRESHOLD) return;
      if (shouldReleaseNativeScroll(deltaY)) {
        releaseToPageScroll();
        return;
      }

      keepNavigationInView();
      moveProjectBy(deltaY > 0 ? 1 : -1);
    },
    { passive: true },
  );

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setGalleryHubState({ modalOpen: null });
      return;
    }

    if (!SCROLL_KEYS.has(event.key)) return;

    const delta = event.key.endsWith("Down") ? 1 : -1;

    if (shouldReleaseNativeScroll(delta)) {
      releaseToPageScroll();
      return;
    }

    event.preventDefault();
    keepNavigationInView();
    moveProjectBy(delta);
  });
}
