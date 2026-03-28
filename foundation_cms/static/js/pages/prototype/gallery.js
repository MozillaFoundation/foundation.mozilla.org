const SELECTORS = {
  item: ".gallery-strip__item",
  navItem: ".gallery-nav__item",
  strip: ".gallery-strip",
  filterContainer: ".gallery-filter-bar__filter",
  filterPanel: ".gallery-filter-bar__panel",
  filterOption: ".gallery-filter-bar__option",
  filterDropdown: ".gallery-filter-bar__dropdown",
  countEl: ".gallery-filter-bar__count",
  activeFilters: ".gallery-active-filters",
  activeFilterChip: ".gallery-active-filter-chip",
};

const CLASS_NAMES = {
  active: "is-active",
  selected: "is-selected",
  activeFilterChip: "gallery-active-filter-chip",
};

const MULTI_SELECT_TYPES = ["topic", "program", "country"];

const items = Array.from(document.querySelectorAll(SELECTORS.item));
const navLinks = Array.from(document.querySelectorAll(SELECTORS.navItem));

// Prebuilt map for constant-time index lookup in the IntersectionObserver callback
const itemIndexMap = new Map(items.map((el, i) => [el, i]));

// Mark the item at `index` as active in both the strip and the sidebar nav.
// Scrolls the nav link into view if it's off-screen within the nav list.
function setActive(index) {
  navLinks.forEach((link, i) => {
    link.classList.toggle(CLASS_NAMES.active, i === index);
  });
  items.forEach((item, i) => {
    item.classList.toggle(CLASS_NAMES.active, i === index);
  });
  navLinks[index]?.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

// Compute an IntersectionObserver rootMargin that centers a detection zone
// equal to the active image height in the viewport.
// This prevents the active item from lingering after its top edge scrolls off screen.
//
// Formula: margin = (vh - activeImageHeight) / 2
// activeImageHeight = strip width × image ratio (active item fills 100% of strip width)
// The ratio is read from the --gallery-image-ratio CSS custom property so it stays in sync with the SCSS $image-ratio variable.
function getScrollspyRootMargin() {
  const strip = document.querySelector(SELECTORS.strip);
  if (!strip) return "-35% 0px -35% 0px";
  const ratio =
    parseFloat(getComputedStyle(strip).getPropertyValue("--gallery-image-ratio")) || 1;
  const activeImageHeight = strip.getBoundingClientRect().width * ratio;
  const vh = window.innerHeight;
  const margin = Math.max(0, (vh - activeImageHeight) / 2);
  return `-${margin}px 0px -${margin}px 0px`;
}

// Scrollspy:
// Watches strip items with IntersectionObserver and calls setActive when an item enters the centered detection zone.
// The observer is recreated on resize so rootMargin stays accurate as the strip width changes.
function initGalleryScrollspy() {
  if (!items.length || !navLinks.length) return;

  let observer;

  // Locked while a click-initiated scroll is in flight so the scrollspy
  // cannot override the intended active item mid-animation.
  let clickScrollLocked = false;
  let clickScrollTimer;
  let scrollSettleTimer;
  let scrollSettleHandler = null;

  // Cancel any in-progress click-scroll sequence.
  function cancelClickScroll() {
    clearTimeout(clickScrollTimer);
    clearTimeout(scrollSettleTimer);
    if (scrollSettleHandler) {
      window.removeEventListener("scroll", scrollSettleHandler);
      scrollSettleHandler = null;
    }
  }

  function createObserver() {
    if (observer) observer.disconnect();
    observer = new IntersectionObserver(
      (entries) => {
        if (clickScrollLocked) return;
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActive(itemIndexMap.get(entry.target));
          }
        });
      },
      {
        rootMargin: getScrollspyRootMargin(),
        threshold: 0,
      },
    );
    items.forEach((item) => observer.observe(item));
  }

  createObserver();

  // Debounced resize handler — rootMargin is in px so it must update when the
  // strip width or viewport height changes.
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(createObserver, 150);
  });

  // Clicking a nav item:
  //   1. Immediately marks it active (instant visual feedback).
  //   2. Waits for the CSS width transition (0.35 s) to finish so the item is
  //      at its full expanded size and the layout has settled.
  //   3. Scrolls so the now-full-size image is centered in the viewport.
  //   4. Re-affirms the intended active item once scrolling stops, then releases
  //      the scrollspy lock.
  //
  // The scrollspy is locked for the duration so it cannot fight the scroll.
  // The lock is released by detecting scroll-end (150 ms of no scroll events)
  // rather than a fixed timeout, so long scrolls to distant items are handled
  // correctly. A 1.5 s fallback handles the case where no scroll fires at all.
  navLinks.forEach((btn, i) => {
    btn.addEventListener("click", () => {
      cancelClickScroll();
      clickScrollLocked = true;

      setActive(i);

      // After the transition the item occupies its full active height, and
      // getBoundingClientRect gives the correct settled position.
      clickScrollTimer = setTimeout(() => {
        const strip = document.querySelector(SELECTORS.strip);
        if (strip) {
          const ratio =
            parseFloat(getComputedStyle(strip).getPropertyValue("--gallery-image-ratio")) || 1;
          const W = strip.getBoundingClientRect().width * ratio;
          const itemTop = items[i].getBoundingClientRect().top + window.scrollY;
          window.scrollTo({
            top: itemTop - (window.innerHeight - W) / 2,
            behavior: "smooth",
          });
        }

        // Release the lock 150 ms after scrolling stops.
        // Re-affirm the intended item first so any slight centering error
        // doesn't let an adjacent item win when the scrollspy resumes.
        scrollSettleHandler = () => {
          clearTimeout(scrollSettleTimer);
          scrollSettleTimer = setTimeout(() => {
            window.removeEventListener("scroll", scrollSettleHandler);
            scrollSettleHandler = null;
            setActive(i);
            clickScrollLocked = false;
          }, 150);
        };
        window.addEventListener("scroll", scrollSettleHandler);

        // Fallback if no scroll events fire (e.g. already at target position).
        scrollSettleTimer = setTimeout(() => {
          window.removeEventListener("scroll", scrollSettleHandler);
          scrollSettleHandler = null;
          clickScrollLocked = false;
        }, 1500);
      }, 350); // matches the CSS `transition: width 0.35s`
    });
  });
}

// Filter bar: manages topic/program/country (multi-select Sets) and year
// (single-select string). Toggling a filter calls applyFilters() which
// shows/hides matching strip items and nav links in sync.
function initFilters() {
  const filterContainers = document.querySelectorAll(SELECTORS.filterContainer);
  const countEl = document.querySelector(SELECTORS.countEl);
  const activeFiltersEl = document.querySelector(SELECTORS.activeFilters);

  if (!filterContainers.length) return;

  const filterState = {
    topic: new Set(),
    program: new Set(),
    country: new Set(),
    year: null,
  };

  filterContainers.forEach((container) => {
    const type = container.dataset.filterType;
    const panel = container.querySelector(SELECTORS.filterPanel);

    panel.querySelectorAll(SELECTORS.filterOption).forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const val = btn.dataset.value;

        if (type === "year") {
          // Year is single-select: clicking the active value deselects it
          if (filterState.year === val) {
            filterState.year = null;
            btn.classList.remove(CLASS_NAMES.selected);
          } else {
            panel
              .querySelectorAll(SELECTORS.filterOption)
              .forEach((b) => b.classList.remove(CLASS_NAMES.selected));
            filterState.year = val;
            btn.classList.add(CLASS_NAMES.selected);
          }
        } else {
          // All other filter types are multi-select Sets
          if (filterState[type].has(val)) {
            filterState[type].delete(val);
            btn.classList.remove(CLASS_NAMES.selected);
          } else {
            filterState[type].add(val);
            btn.classList.add(CLASS_NAMES.selected);
          }
        }

        panel.setAttribute("hidden", "");
        updateDropdownLabel(container, type);
        applyFilters();
        renderActiveFilters();
      });
    });

    // Show on hover; delay close so the cursor can cross the gap into the panel
    const dropdownBtn = container.querySelector(SELECTORS.filterDropdown);
    let closeTimer;
    const openPanel = () => {
      clearTimeout(closeTimer);
      panel.removeAttribute("hidden");
      dropdownBtn.classList.add("is-open");
    };
    const closePanel = () => {
      closeTimer = setTimeout(() => {
        panel.setAttribute("hidden", "");
        dropdownBtn.classList.remove("is-open");
      }, 150);
    };

    container.addEventListener("mouseenter", openPanel);
    container.addEventListener("mouseleave", closePanel);
    panel.addEventListener("mouseenter", openPanel);
    panel.addEventListener("mouseleave", closePanel);
  });

  // Update the dropdown button label to show how many options are selected.
  function updateDropdownLabel(container, type) {
    const btn = container.querySelector(SELECTORS.filterDropdown);
    const label = btn.dataset.label;
    const count =
      type === "year" ? (filterState.year !== null ? 1 : 0) : filterState[type].size;
    btn.textContent = count > 0 ? `${label} (${count})` : label;
  }

  // Re-render the active filter chips below the filter bar.
  function renderActiveFilters() {
    if (!activeFiltersEl) return;

    const chips = [];
    MULTI_SELECT_TYPES.forEach((type) => {
      filterState[type].forEach((val) => chips.push({ type, val }));
    });
    if (filterState.year !== null) {
      chips.push({ type: "year", val: filterState.year });
    }

    activeFiltersEl.innerHTML = chips
      .map(
        ({ type, val }) =>
          `<button class="${CLASS_NAMES.activeFilterChip}" data-type="${type}" data-value="${val}">${val} <span aria-hidden="true">×</span></button>`,
      )
      .join("");

    activeFiltersEl.querySelectorAll(SELECTORS.activeFilterChip).forEach((chip) => {
      chip.addEventListener("click", () => {
        const { type, value } = chip.dataset;

        if (type === "year") {
          filterState.year = null;
        } else {
          filterState[type].delete(value);
        }

        // Sync the deselected state back into the panel
        const fc = Array.from(filterContainers).find(
          (c) => c.dataset.filterType === type,
        );
        if (fc) {
          fc.querySelectorAll(SELECTORS.filterOption).forEach((opt) => {
            if (opt.dataset.value === value) opt.classList.remove(CLASS_NAMES.selected);
          });
          updateDropdownLabel(fc, type);
        }

        applyFilters();
        renderActiveFilters();
      });
    });
  }

  // Show/hide strip items and nav links based on the current filterState.
  // All active filter types must match (AND logic); an empty Set matches everything.
  function applyFilters() {
    let visibleCount = 0;

    navLinks.forEach((navItem, i) => {
      const stripItem = items[i];
      const tags = navItem.dataset.tags
        ? navItem.dataset.tags.split(",").map((t) => t.trim())
        : [];

      const topicMatch =
        filterState.topic.size === 0 ||
        [...filterState.topic].every((t) => tags.includes(t));
      const programMatch =
        filterState.program.size === 0 ||
        [...filterState.program].every((p) => navItem.dataset.program === p);
      const countryMatch =
        filterState.country.size === 0 ||
        [...filterState.country].every((c) => navItem.dataset.country === c);
      const yearMatch =
        filterState.year === null || navItem.dataset.year === filterState.year;

      const visible = topicMatch && programMatch && countryMatch && yearMatch;

      const li = navItem.closest("li");
      if (li) li.style.display = visible ? "" : "none";
      if (stripItem) stripItem.style.display = visible ? "" : "none";

      if (visible) visibleCount++;
    });

    if (countEl) countEl.textContent = `${visibleCount} projects`;

    // Activate the first visible item
    const firstVisible = navLinks.findIndex(
      (n) => n.closest("li")?.style.display !== "none",
    );
    if (firstVisible >= 0) setActive(firstVisible);
  }
}

initGalleryScrollspy();
initFilters();
