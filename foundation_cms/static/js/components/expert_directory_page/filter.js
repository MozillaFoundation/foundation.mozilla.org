const DEBOUNCE_MS = 200;

const SELECTORS = {
  form: "#expert-filter-form",
  toggle: "[data-filter-toggle]",
  closeBtn: "[data-expert-filter-close]",
  resetBtn: "[data-expert-filter-reset]",
  debug: "#expert-filter-debug",
  checkbox: "input[type='checkbox']",
  toggleLabel: ".expert-filter__toggle-label",
  listing: "#listing",
};

/**
 * Returns all URL param keys that should be cleared on filter submission:
 * the checkbox field names derived from the form, plus the pagination param
 * from `data-page-param` so results always start at page 1.
 *
 * @param {HTMLFormElement} form
 * @param {HTMLInputElement[]} checkboxes
 * @returns {string[]}
 */
function getFilterKeys(form, checkboxes) {
  const keys = new Set(checkboxes.map((el) => el.name));
  // strip the pagination param so filtered results always start at page 1
  const pageParam = form.dataset.pageParam;

  if (pageParam) keys.add(pageParam);

  return [...keys];
}

/**
 * Builds a clean URL from the current form state: resets filter params,
 * preserves everything else (e.g. language prefix), and omits empty values.
 *
 * @param {HTMLFormElement} form
 * @param {HTMLInputElement[]} checkboxes
 * @returns {URL}
 */
function buildFilterUrl(form, checkboxes) {
  const url = new URL(window.location.href);
  const data = new FormData(form);

  getFilterKeys(form, checkboxes).forEach((key) => url.searchParams.delete(key));

  for (const [key, value] of data.entries()) {
    if (value) url.searchParams.append(key, value);
  }

  return url;
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
 * the close button (collapses all open panels), and the reset button
 * (clears all checkboxes). Auto-submits on checkbox change via a debounced
 * fetch that swaps only the listing section without a full page reload.
 */
export function initExpertFilter() {
  const form = document.querySelector(SELECTORS.form);
  if (!form) return;

  const toggles = Array.from(form.querySelectorAll(SELECTORS.toggle));
  const checkboxes = Array.from(form.querySelectorAll(SELECTORS.checkbox));
  const closeBtn = form.querySelector(SELECTORS.closeBtn);
  const resetBtn = form.querySelector(SELECTORS.resetBtn);
  let debounceTimer = null;
  let abortController = null;

  updateDebug(form);
  updateToggleCounts(toggles);

  function anyPanelOpen() {
    return toggles.some((t) => t.getAttribute("aria-expanded") === "true");
  }

  function syncCloseBtn() {
    if (!closeBtn) return;
    closeBtn.hidden = !anyPanelOpen();
  }

  function syncResetBtn() {
    if (!resetBtn) return;
    const anyChecked = checkboxes.some((cb) => cb.checked);
    resetBtn.hidden = !(anyChecked && !anyPanelOpen());
  }

  syncCloseBtn();
  syncResetBtn();

  closeBtn?.addEventListener("click", () => {
    closeAllPanels(toggles);
    syncCloseBtn();
    syncResetBtn();
  });

  resetBtn?.addEventListener("click", () => {
    checkboxes.forEach((cb) => {
      cb.checked = false;
    });
    form.dispatchEvent(new Event("change"));
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

      syncCloseBtn();
      syncResetBtn();
    });
  });

  async function fetchListing() {
    if (abortController) abortController.abort();
    abortController = new AbortController();

    const url = buildFilterUrl(form, checkboxes);
    const listing = document.querySelector(SELECTORS.listing);

    if (listing) listing.classList.add("is-loading");

    try {
      const response = await fetch(url.toString(), {
        headers: { "X-Requested-With": "XMLHttpRequest" },
        signal: abortController.signal,
      });

      if (!response.ok) return;

      const html = await response.text();

      if (listing) listing.outerHTML = html;

      history.pushState(null, "", url.toString());

      // Sync the debug panel count from the freshly rendered listing
      const newListing = document.querySelector(SELECTORS.listing);
      const debugEl = document.querySelector(SELECTORS.debug);

      if (debugEl && newListing) {
        debugEl.dataset.totalCount = newListing.dataset.totalCount;
        updateDebug(form);
      }
    } catch (err) {
      if (listing) listing.classList.remove("is-loading");
      if (err.name !== "AbortError") throw err;
    }
  }

  form.addEventListener("change", () => {
    updateDebug(form);
    updateToggleCounts(toggles);
    syncResetBtn();

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(fetchListing, DEBOUNCE_MS);
  });
}
