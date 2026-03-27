const SELECTORS = {
  item: ".gallery-strip__item",
  navItem: ".gallery-nav__item",
  filterContainer: ".gallery-filter-bar__filter",
  countEl: ".gallery-filter-bar__count",
  activeFilters: ".gallery-active-filters",
};

const CLASS_NAMES = {
  active: "is-active",
  selected: "is-selected",
};

const items = Array.from(document.querySelectorAll(SELECTORS.item));
const navLinks = Array.from(document.querySelectorAll(SELECTORS.navItem));

function setActive(index) {
  navLinks.forEach((link, i) => {
    link.classList.toggle(CLASS_NAMES.active, i === index);
  });
  items.forEach((item, i) => {
    item.classList.toggle(CLASS_NAMES.active, i === index);
  });
  navLinks[index]?.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function initGalleryScrollspy() {
  if (!items.length || !navLinks.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          setActive(items.indexOf(entry.target));
        }
      });
    },
    {
      rootMargin: "-35% 0px -35% 0px",
      threshold: 0,
    },
  );

  items.forEach((item) => observer.observe(item));

  navLinks.forEach((btn, i) => {
    btn.addEventListener("click", () => {
      items[i]?.scrollIntoView({ behavior: "smooth" });
    });
  });
}

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
    const panel = container.querySelector(".gallery-filter-bar__panel");

    panel.querySelectorAll(".gallery-filter-bar__option").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const val = btn.dataset.value;

        if (type === "year") {
          if (filterState.year === val) {
            filterState.year = null;
            btn.classList.remove(CLASS_NAMES.selected);
          } else {
            panel
              .querySelectorAll(".gallery-filter-bar__option")
              .forEach((b) => b.classList.remove(CLASS_NAMES.selected));
            filterState.year = val;
            btn.classList.add(CLASS_NAMES.selected);
          }
        } else {
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
    const dropdownBtn = container.querySelector(".gallery-filter-bar__dropdown");
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

  function updateDropdownLabel(container, type) {
    const btn = container.querySelector(".gallery-filter-bar__dropdown");
    const label = btn.dataset.label;
    const count =
      type === "year" ? (filterState.year !== null ? 1 : 0) : filterState[type].size;
    btn.textContent = count > 0 ? `${label} (${count})` : label;
  }

  function renderActiveFilters() {
    if (!activeFiltersEl) return;

    const chips = [];
    ["topic", "program", "country"].forEach((type) => {
      filterState[type].forEach((val) => chips.push({ type, val }));
    });
    if (filterState.year !== null) {
      chips.push({ type: "year", val: filterState.year });
    }

    activeFiltersEl.innerHTML = chips
      .map(
        ({ type, val }) =>
          `<button class="gallery-active-filter-chip" data-type="${type}" data-value="${val}">${val} <span aria-hidden="true">×</span></button>`,
      )
      .join("");

    activeFiltersEl.querySelectorAll(".gallery-active-filter-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        const { type, value } = chip.dataset;

        if (type === "year") {
          filterState.year = null;
        } else {
          filterState[type].delete(value);
        }

        // Sync the deselected state back into the panel
        const fc = document.querySelector(`[data-filter-type="${type}"]`);
        if (fc) {
          fc.querySelectorAll(".gallery-filter-bar__option").forEach((opt) => {
            if (opt.dataset.value === value) opt.classList.remove(CLASS_NAMES.selected);
          });
          updateDropdownLabel(fc, type);
        }

        applyFilters();
        renderActiveFilters();
      });
    });
  }

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
