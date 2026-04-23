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

const strip = document.querySelector(SELECTORS.strip);
const items = Array.from(document.querySelectorAll(SELECTORS.item));
const navLinks = Array.from(document.querySelectorAll(SELECTORS.navItem));

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

// Scrollspy:
// On each scroll tick, finds the visible item whose center is closest to the
// viewport center and marks it active. More robust than IntersectionObserver
// for this use case — re-evaluates current state on every frame rather than
// relying on edge-triggered intersection events.
function initGalleryScrollspy() {
  if (!items.length || !navLinks.length) return;

  // Height of the sticky primary nav — read from scroll-margin-top already set on strip items.
  // Used to center the active item in the visible area below the nav rather than the raw viewport center.
  const navHeight = parseFloat(getComputedStyle(items[0]).scrollMarginTop) || 0;

  // Locked while a click-initiated scroll is in flight so the scrollspy
  // cannot override the intended active item mid-animation.
  let scrollLocked = false;
  let scrollSettleTimer;
  let scrollSettleHandler = null;

  // Cancel any in-progress click-scroll sequence.
  function cancelClickScroll() {
    clearTimeout(scrollSettleTimer);
    if (scrollSettleHandler) {
      window.removeEventListener("scroll", scrollSettleHandler);
      scrollSettleHandler = null;
    }
  }

  // Find the visible item whose center is closest to the visible-area center and activate it.
  function onScroll() {
    if (scrollLocked) return;
    const viewportCenter = (window.innerHeight + navHeight) / 2;
    let bestIndex = -1;
    let bestDist = Infinity;
    items.forEach((item, i) => {
      if (item.style.display === "none") return;
      const rect = item.getBoundingClientRect();
      const dist = Math.abs(rect.top + rect.height / 2 - viewportCenter);
      if (dist < bestDist) {
        bestDist = dist;
        bestIndex = i;
      }
    });
    if (bestIndex >= 0) setActive(bestIndex);
  }

  window.addEventListener("scroll", onScroll, { passive: true });

  // Hovering a nav item:
  //   1. Computes item i's final document-top after the CSS width transition.
  //      If the currently-active item is above i it will shrink (100% → 40%,
  //      −0.6 W), shifting i upward by a known amount.
  //   2. Simultaneously calls setActive(i) and scrolls to the pre-computed
  //      target — the width transition and the scroll run concurrently,
  //      so the image expands while moving rather than expanding then jumping.
  //   3. Re-affirms the intended active item once scrolling stops, then
  //      releases the scrollspy lock.
  navLinks.forEach((btn, i) => {
    btn.addEventListener("mouseenter", () => {
      cancelClickScroll();
      scrollLocked = true;

      if (!strip) {
        scrollLocked = false;
        return;
      }

      const ratio =
        parseFloat(
          getComputedStyle(strip).getPropertyValue("--gallery-image-ratio"),
        ) || 1;
      const W = strip.getBoundingClientRect().width * ratio;

      // Pre-compute item i's final position before the transition mutates the layout.
      const prevActive = items.findIndex((item) =>
        item.classList.contains(CLASS_NAMES.active),
      );
      let itemDocTop = items[i].getBoundingClientRect().top + window.scrollY;
      if (prevActive >= 0 && prevActive < i) {
        itemDocTop -= 0.6 * W; // prev active shrinks: 100% → 40%
      }

      setActive(i);
      window.scrollTo({
        top: itemDocTop + W / 2 - (window.innerHeight + navHeight) / 2,
        behavior: "smooth",
      });

      // Release the lock 150 ms after scrolling stops.
      // Re-affirm the intended item so any residual centering error
      // doesn't let an adjacent item win when the scrollspy resumes.
      scrollSettleHandler = () => {
        clearTimeout(scrollSettleTimer);
        scrollSettleTimer = setTimeout(() => {
          window.removeEventListener("scroll", scrollSettleHandler);
          scrollSettleHandler = null;
          setActive(i);
          scrollLocked = false;
        }, 150);
      };
      window.addEventListener("scroll", scrollSettleHandler);

      // Fallback if no scroll events fire (e.g. already at target position).
      scrollSettleTimer = setTimeout(() => {
        window.removeEventListener("scroll", scrollSettleHandler);
        scrollSettleHandler = null;
        scrollLocked = false;
      }, 1500);
    });
  });

  // Set initial active item based on current scroll/layout position.
  onScroll();
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

    // Show on click; close when clicking outside
    const dropdownBtn = container.querySelector(SELECTORS.filterDropdown);
    const openPanel = () => {
      panel.removeAttribute("hidden");
      dropdownBtn.classList.add("is-open");
    };
    const closePanel = () => {
      panel.setAttribute("hidden", "");
      dropdownBtn.classList.remove("is-open");
    };
    const togglePanel = () => {
      if (panel.hasAttribute("hidden")) {
        // Close any other open panels first
        filterContainers.forEach((other) => {
          if (other !== container) {
            other
              .querySelector(SELECTORS.filterPanel)
              ?.setAttribute("hidden", "");
            other
              .querySelector(SELECTORS.filterDropdown)
              ?.classList.remove("is-open");
          }
        });
        openPanel();
      } else {
        closePanel();
      }
    };

    dropdownBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      togglePanel();
    });

    document.addEventListener("click", (e) => {
      if (!container.contains(e.target)) closePanel();
    });
  });

  // Update the dropdown button label to show how many options are selected.
  function updateDropdownLabel(container, type) {
    const btn = container.querySelector(SELECTORS.filterDropdown);
    const label = btn.dataset.label;
    const count =
      type === "year"
        ? filterState.year !== null
          ? 1
          : 0
        : filterState[type].size;
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

    activeFiltersEl
      .querySelectorAll(SELECTORS.activeFilterChip)
      .forEach((chip) => {
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
              if (opt.dataset.value === value)
                opt.classList.remove(CLASS_NAMES.selected);
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

    const allCleared =
      MULTI_SELECT_TYPES.every((t) => filterState[t].size === 0) &&
      filterState.year === null;

    if (allCleared) {
      // Full list restored — reset to top so item 0 is centred, matching the initial load state.
      setActive(0);
      setStripTopMargin();
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      // Activate the first visible item in the filtered list.
      const firstVisible = navLinks.findIndex(
        (n) => n.closest("li")?.style.display !== "none",
      );
      if (firstVisible >= 0) setActive(firstVisible);
    }
  }
}

// Set strip margin-top so item 0's center aligns with the scrollspy detection
// center ((innerHeight + navHeight) / 2) when scrollY = 0. Item 0 must already
// be active (width = 100%) before calling so the height measurement is correct.
function setStripTopMargin() {
  if (!strip || !items.length) return;
  strip.style.marginTop = ""; // reset before measuring natural position
  const ratio =
    parseFloat(
      getComputedStyle(strip).getPropertyValue("--gallery-image-ratio"),
    ) || 1;
  const W = strip.getBoundingClientRect().width * ratio;
  const navH = parseFloat(getComputedStyle(items[0]).scrollMarginTop) || 0;
  const item0DocTop = items[0].getBoundingClientRect().top + window.scrollY;
  strip.style.marginTop = `${Math.max(0, (window.innerHeight + navH) / 2 - item0DocTop - W / 2)}px`;
}

setActive(0);
setStripTopMargin();
window.scrollTo({ top: 0, behavior: "instant" });
initGalleryScrollspy(); // calls onScroll() internally to set initial active item
initFilters();

// ResizeObserver fires when the strip's dimensions change (window resize, font
// scaling, layout shifts) without needing a debounce timer. Changing marginTop
// doesn't affect the strip's border-box size so there's no feedback loop.
// Only recalculate when the strip's WIDTH changes (viewport resize).
// Height changes from item transitions also fire ResizeObserver — calling
// setStripTopMargin mid-scroll would abruptly reset marginTop and cause jumps.
let _lastStripWidth = strip?.getBoundingClientRect().width ?? 0;
new ResizeObserver((entries) => {
  const w = entries[0].contentRect.width;
  if (w !== _lastStripWidth) {
    _lastStripWidth = w;
    setStripTopMargin();
  }
}).observe(strip);

// Reveal the strip now that positions are set and the initial active item is determined.
requestAnimationFrame(() => {
  strip?.classList.add("is-ready");
});
