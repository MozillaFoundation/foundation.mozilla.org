const SELECTORS = {
  form: "#expert-filter-form",
  toggle: "[data-filter-toggle]",
  debug: "#expert-filter-debug",
  checkbox: 'input[type="checkbox"]',
  toggleLabel: ".expert-filter__toggle-label",
};

/**
 * Returns all URL param keys that should be cleared on filter submission:
 * the checkbox field names derived from the form, plus the pagination param
 * from `data-page-param` so results always start at page 1.
 *
 * @param {HTMLFormElement} form
 * @returns {string[]}
 */
function getFilterKeys(form) {
  const keys = new Set(
    Array.from(form.querySelectorAll(SELECTORS.checkbox)).map((el) => el.name),
  );
  // strip the pagination param so filtered results always start at page 1
  const pageParam = form.dataset.pageParam;
  if (pageParam) keys.add(pageParam);
  return [...keys];
}

/**
 * Updates the debug panel with the current expert count and active filter state.
 *
 * @param {HTMLFormElement} form
 */
function updateDebug(form) {
  const el = document.querySelector(SELECTORS.debug);
  if (!el) return;
  const data = new FormData(form);
  const params = {};
  for (const [key, value] of data.entries()) {
    if (!value) continue;
    if (Object.prototype.hasOwnProperty.call(params, key)) {
      if (!Array.isArray(params[key])) params[key] = [params[key]];
      params[key].push(value);
    } else {
      params[key] = value;
    }
  }
  const count = el.dataset.totalCount ?? "?";
  const filterState = Object.keys(params).length
    ? JSON.stringify(params, null, 2)
    : "(no active filters)";
  el.textContent = `${count} experts\n\n${filterState}`;
}

/**
 * Updates each toggle button label to reflect the number of checked options in its panel,
 * e.g. "Country (3)". Resets to the base label when none are checked.
 *
 * @param {Element[]} toggles
 */
function updateToggleCounts(toggles) {
  toggles.forEach((toggle) => {
    const panelId = toggle.getAttribute("aria-controls");
    const panel = document.getElementById(panelId);
    const labelEl = toggle.querySelector(SELECTORS.toggleLabel);
    if (!panel || !labelEl) return;
    const count = panel.querySelectorAll(
      `${SELECTORS.checkbox}:checked`,
    ).length;
    const base = labelEl.dataset.baseLabel;
    labelEl.textContent = count > 0 ? `${base} (${count})` : base;
  });
}

/**
 * Collapses all filter panels and resets their toggle buttons to aria-expanded="false".
 *
 * @param {Element[]} toggles
 */
function closeAllPanels(toggles) {
  toggles.forEach((toggle) => {
    toggle.setAttribute("aria-expanded", "false");
    const panelId = toggle.getAttribute("aria-controls");
    const panel = document.getElementById(panelId);
    if (panel) panel.setAttribute("hidden", "");
  });
}

/**
 * Initializes the expert directory filter form: wires up toggle buttons,
 * checkbox change handlers, and form submission with clean URL building.
 */
export function initExpertFilter() {
  const form = document.querySelector(SELECTORS.form);
  if (!form) return;

  const toggles = Array.from(form.querySelectorAll(SELECTORS.toggle));

  updateDebug(form);
  updateToggleCounts(toggles);
  form.addEventListener("change", () => {
    updateDebug(form);
    updateToggleCounts(toggles);
  });

  toggles.forEach((toggle) => {
    const panelId = toggle.getAttribute("aria-controls");
    const panel = document.getElementById(panelId);
    if (!panel) return;

    toggle.addEventListener("click", () => {
      const isExpanded = toggle.getAttribute("aria-expanded") === "true";

      closeAllPanels(toggles);

      if (!isExpanded) {
        toggle.setAttribute("aria-expanded", "true");
        panel.removeAttribute("hidden");
      }
    });
  });

  // strip empty filter params from the GET request so the URL stays clean
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const url = new URL(window.location.href);
    const data = new FormData(form);

    // reset filter params, preserve everything else (e.g. page lang prefix)
    getFilterKeys(form).forEach((key) => url.searchParams.delete(key));

    for (const [key, value] of data.entries()) {
      if (value) url.searchParams.append(key, value);
    }

    window.location.assign(url.toString());
  });
}
