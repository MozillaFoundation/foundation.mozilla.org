/**
 * Search results filter and sort controls.
 *
 * @module searchPageFilterControls
 */

const PREVIEW_DEBOUNCE_MS = 200;
const LARGE_VIEWPORT_QUERY = "(min-width: 64em)";

const CLASSNAMES = {
  drawerOpen: "search-filter-drawer-open",
};

const SELECTORS = {
  root: "[data-search-results-page]",
  form: "[data-search-filter-form]",
  drawer: "[data-search-drawer]",
  drawerOpen: "[data-search-drawer-open]",
  drawerClose: "[data-search-drawer-close]",
  drawerReset: "[data-search-drawer-reset]",
  drawerApply: "[data-search-drawer-apply]",
  topicLabel: "[data-search-topic-label]",
};

const DATA_KEYS = {
  topicWasChecked: "searchTopicWasChecked",
};

const FOCUSABLE_SELECTOR = [
  "a[href]",
  "button:not([disabled])",
  "input:not([disabled])",
  "select:not([disabled])",
  "textarea:not([disabled])",
  '[tabindex]:not([tabindex="-1"])',
].join(",");

/**
 * Builds a clean search URL from the current filter form.
 *
 * The search endpoint is the source of truth for filtering. This helper keeps
 * the submitted query/filter/sort values, drops pagination, and omits empty
 * fields so a filter change always restarts at page 1.
 *
 * @param {HTMLFormElement} form
 * @returns {URL}
 */
function buildUrlFromForm(form) {
  const url = new URL(form.action, window.location.origin);
  const formData = new FormData(form);

  formData.delete("page");

  for (const [key, value] of formData.entries()) {
    if (value) url.searchParams.append(key, value);
  }

  return url;
}

/**
 * Navigates to the URL represented by the current filter form state.
 *
 * @param {HTMLFormElement} form
 */
function submitForm(form) {
  window.location.assign(buildUrlFromForm(form).toString());
}

/**
 * Updates the mobile/tablet drawer apply button with the result count preview.
 *
 * @param {HTMLElement | null} button
 * @param {string | number} count
 */
function setApplyButtonLabel(button, count) {
  if (!button) return;

  const label = button.dataset.searchDrawerApplyLabel || "Display results";

  button.textContent = `${label} (${count})`;
}

/**
 * Returns the drawer form to its default filter state.
 *
 * @param {HTMLFormElement} form
 */
function resetDrawerForm(form) {
  const contentAll = form.querySelector(
    'input[name="content_type"][value="all"]',
  );
  const sortRelevance = form.querySelector(
    'input[name="sort"][value="relevance"]',
  );
  const topics = form.querySelectorAll('input[name="topic"]');

  if (contentAll) contentAll.checked = true;
  if (sortRelevance) sortRelevance.checked = true;
  topics.forEach((topic) => {
    topic.checked = false;
  });
}

/**
 * Stores whether a topic radio was selected before the click interaction
 * changes its checked state. Radio labels can dispatch click events after the
 * input has already toggled, so this lets selected pills be clicked again to
 * clear without clearing newly-selected pills.
 *
 * @param {Element} label
 */
function rememberTopicCheckedState(label) {
  const input = label.querySelector('input[name="topic"]');

  label.dataset[DATA_KEYS.topicWasChecked] = input?.checked ? "true" : "false";
}

/**
 * Keeps keyboard focus within an open modal drawer.
 *
 * @param {KeyboardEvent} event
 * @param {HTMLElement} drawer
 */
function trapDrawerFocus(event, drawer) {
  if (event.key !== "Tab") return;

  const focusable = Array.from(
    drawer.querySelectorAll(FOCUSABLE_SELECTOR),
  ).filter((element) => element.getClientRects().length > 0);

  if (!focusable.length) {
    event.preventDefault();
    return;
  }

  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

/**
 * Initializes search result filter controls.
 *
 * Desktop forms submit immediately when content type, topic, or sort changes.
 * Mobile/tablet controls live in a drawer: changing options previews the result
 * count, while the form submit applies the selected filters.
 */
export function initSearchPageFilters() {
  const root = document.querySelector(SELECTORS.root);

  if (!root) return;

  const forms = Array.from(root.querySelectorAll(SELECTORS.form));
  const drawer = root.querySelector(SELECTORS.drawer);
  const drawerOpen = root.querySelector(SELECTORS.drawerOpen);
  const drawerForm = drawer?.querySelector(SELECTORS.form);
  const drawerApply = drawer?.querySelector(SELECTORS.drawerApply);
  const largeViewport = window.matchMedia(LARGE_VIEWPORT_QUERY);
  let lastFocusedElement = null;
  let previewTimer = null;
  let previewAbortController = null;

  // The transformed page-transition wrapper creates a containing block for
  // fixed descendants in WebKit, so place the modal directly under the body.
  if (drawer) document.body.append(drawer);

  /**
   * Locks document scrolling while the full-page filter drawer is open.
   * Class-based overflow containment avoids offsetting nested fixed elements
   * by the current scroll position in iOS Safari.
   *
   * @param {boolean} isLocked
   */
  function setDrawerScrollLock(isLocked) {
    const rootElement = document.documentElement;
    const body = document.body;

    rootElement.classList.toggle(CLASSNAMES.drawerOpen, isLocked);
    body.classList.toggle(CLASSNAMES.drawerOpen, isLocked);
  }

  /**
   * Fetches the filtered search page and reads its total count for the drawer
   * apply CTA. The actual result list is not replaced until the user submits
   * the drawer form.
   */
  function updateDrawerPreview() {
    if (!drawerForm || !drawerApply) return;

    clearTimeout(previewTimer);
    previewTimer = setTimeout(async () => {
      if (previewAbortController) previewAbortController.abort();
      previewAbortController = new AbortController();

      try {
        const response = await fetch(buildUrlFromForm(drawerForm).toString(), {
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-Search-Preview": "true",
          },
          signal: previewAbortController.signal,
        });

        if (!response.ok) return;

        const html = await response.text();
        const doc = new DOMParser().parseFromString(html, "text/html");
        const previewRoot = doc.querySelector(SELECTORS.root);
        const count = previewRoot?.dataset.totalResults;

        if (count !== undefined) setApplyButtonLabel(drawerApply, count);
      } catch (err) {
        if (err.name === "AbortError") return;

        // Keep the last known count when the preview request is unavailable.
      }
    }, PREVIEW_DEBOUNCE_MS);
  }

  /**
   * Opens the filter drawer and moves focus to the close button.
   */
  function openDrawer() {
    if (!drawer || !drawerOpen) return;

    lastFocusedElement = document.activeElement;
    drawer.hidden = false;
    drawerOpen.setAttribute("aria-expanded", "true");
    setDrawerScrollLock(true);
    drawer.querySelector(SELECTORS.drawerClose)?.focus({ preventScroll: true });
  }

  /**
   * Closes the filter drawer and restores focus to the opener when possible.
   */
  function closeDrawer() {
    if (!drawer || !drawerOpen) return;

    drawer.hidden = true;
    drawerOpen.setAttribute("aria-expanded", "false");
    setDrawerScrollLock(false);

    if (
      lastFocusedElement instanceof HTMLElement &&
      lastFocusedElement.getClientRects().length > 0
    ) {
      lastFocusedElement.focus({ preventScroll: true });
    }
  }

  forms.forEach((form) => {
    const mode = form.dataset.searchFilterMode;

    form.querySelectorAll(SELECTORS.topicLabel).forEach((label) => {
      label.addEventListener("pointerdown", () => {
        rememberTopicCheckedState(label);
      });

      label.addEventListener("keydown", (event) => {
        if (event.key !== " " && event.key !== "Enter") return;

        rememberTopicCheckedState(label);
      });

      label.addEventListener("click", (event) => {
        const input = label.querySelector('input[name="topic"]');
        const wasChecked = label.dataset[DATA_KEYS.topicWasChecked] === "true";

        if (!input || !wasChecked) return;

        event.preventDefault();
        input.checked = false;
        label.dataset[DATA_KEYS.topicWasChecked] = "false";

        if (mode === "immediate") {
          submitForm(form);
        } else {
          updateDrawerPreview();
        }
      });
    });

    form.addEventListener("change", () => {
      if (mode === "immediate") {
        submitForm(form);
        return;
      }

      updateDrawerPreview();
    });
  });

  drawerOpen?.addEventListener("click", openDrawer);

  largeViewport.addEventListener("change", (event) => {
    if (event.matches && drawer && !drawer.hidden) closeDrawer();
  });

  drawer?.querySelectorAll(SELECTORS.drawerClose).forEach((button) => {
    button.addEventListener("click", closeDrawer);
  });

  drawer
    ?.querySelector(SELECTORS.drawerReset)
    ?.addEventListener("click", () => {
      if (!drawerForm) return;

      resetDrawerForm(drawerForm);
      updateDrawerPreview();
    });

  drawer?.addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      trapDrawerFocus(event, drawer);
      return;
    }

    if (event.key !== "Escape") return;

    event.preventDefault();
    closeDrawer();
  });
}
