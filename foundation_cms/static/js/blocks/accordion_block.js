// Smooth open and close for Cosmos accordion rows (<details class="mzf-c-accordion-item">).
// Ported from the behavior script in LP's components/elements/accordion/item/index.html,
// LP commit d9c715e96d. Same motion as LP's script, restructured as an ES module:
// pending animations are tracked in WeakMaps instead of properties on the element,
// the two transitionend/fallback blocks share one helper, and LP's unused
// motionTokens/closeDurationMs helpers are dropped.
//
// Without this script the rows still open and close, instantly, because <details>
// does that itself.

const SELECTORS = {
  group: ".mzf-c-accordion-group",
  item: ".mzf-c-accordion-item",
  summary: ".mzf-c-accordion-item__summary",
  reveal: ".mzf-c-accordion-item__reveal",
};

const CLASSES = {
  expanding: "mzf-c-accordion-item--expanding",
  collapsing: "mzf-c-accordion-item--collapsing",
};

// Extra time after the transition before finishing anyway, in case transitionend
// never fires (e.g. the row is hidden mid-animation).
const FALLBACK_BUFFER_MS = 48;

// Pending finish callbacks per row, so a click mid-animation can settle the one
// in flight before starting the next.
const pendingExpand = new WeakMap();
const pendingCollapse = new WeakMap();

function ms(value, fallback) {
  const n = parseFloat(String(value || "").trim());
  return Number.isFinite(n) ? n : fallback;
}

function expandMotion(details) {
  const styles = getComputedStyle(details);
  return {
    expandMs: ms(
      styles.getPropertyValue("--mzf-accordion-expand-duration"),
      500,
    ),
    expandEase:
      styles.getPropertyValue("--mzf-accordion-expand-ease").trim() || "ease",
  };
}

function collapseMotion(details) {
  const styles = getComputedStyle(details);
  return {
    collapseMs: ms(
      styles.getPropertyValue("--mzf-accordion-collapse-duration"),
      400,
    ),
    collapseEase:
      styles.getPropertyValue("--mzf-accordion-collapse-ease").trim() || "ease",
  };
}

function clearRevealInlineStyles(reveal) {
  reveal.style.transition = "";
  reveal.style.gridTemplateRows = "";
  reveal.style.height = "";
  reveal.style.overflow = "";
}

function cancelPendingMotion(details, reveal) {
  pendingExpand.get(details)?.();
  pendingCollapse.get(details)?.();
  clearRevealInlineStyles(reveal);
  details.classList.remove(CLASSES.collapsing);
  details.classList.remove(CLASSES.expanding);
}

// Calls finish once, on the reveal's own height transitionend or after the
// fallback timeout, whichever comes first.
function onHeightTransitionEnd(reveal, durationMs, finish) {
  let finished = false;
  let fallback;

  const done = () => {
    if (finished) return;
    finished = true;
    reveal.removeEventListener("transitionend", onEnd);
    window.clearTimeout(fallback);
    finish();
  };
  const onEnd = (event) => {
    if (event.target !== reveal || event.propertyName !== "height") return;
    done();
  };

  reveal.addEventListener("transitionend", onEnd);
  fallback = window.setTimeout(done, durationMs + FALLBACK_BUFFER_MS);
  return done;
}

export function expand(details, reveal) {
  cancelPendingMotion(details, reveal);
  details.classList.add(CLASSES.expanding);
  const { expandMs, expandEase } = expandMotion(details);
  const targetHeight = reveal.scrollHeight;

  // Lock height before [open] so grid 1fr cannot paint a full frame.
  reveal.style.transition = "none";
  reveal.style.gridTemplateRows = "none";
  reveal.style.height = "0px";
  reveal.style.overflow = "visible";
  void reveal.offsetHeight;

  details.open = true;
  void reveal.offsetHeight;

  reveal.style.transition = `height ${expandMs}ms ${expandEase}`;
  reveal.style.height = `${targetHeight}px`;

  const done = onHeightTransitionEnd(reveal, expandMs, () => {
    clearRevealInlineStyles(reveal);
    details.classList.remove(CLASSES.expanding);
    pendingExpand.delete(details);
  });
  pendingExpand.set(details, done);
}

export function collapse(details, reveal) {
  cancelPendingMotion(details, reveal);
  const { collapseMs, collapseEase } = collapseMotion(details);
  details.classList.add(CLASSES.collapsing);

  // Height-driven close keeps copy visible inside the clip.
  const startHeight = reveal.getBoundingClientRect().height;
  reveal.style.transition = "none";
  reveal.style.gridTemplateRows = "none";
  reveal.style.height = `${startHeight}px`;
  reveal.style.overflow = "clip";
  void reveal.offsetHeight;
  reveal.style.transition = `height ${collapseMs}ms ${collapseEase}`;
  reveal.style.height = "0px";

  const done = onHeightTransitionEnd(reveal, collapseMs, () => {
    details.open = false;
    clearRevealInlineStyles(reveal);
    requestAnimationFrame(() => {
      details.classList.remove(CLASSES.collapsing);
    });
    pendingCollapse.delete(details);
  });
  pendingCollapse.set(details, done);
}

// The other rows in the same group that are open, or opening, and not already closing.
function openSiblings(details) {
  const group = details.closest(SELECTORS.group);
  if (!group) return [];

  return [...group.querySelectorAll(SELECTORS.item)].filter(
    (row) =>
      row !== details &&
      row.open &&
      !row.classList.contains(CLASSES.collapsing),
  );
}

export function initAccordionItem(details) {
  if (details.dataset.mzfAccordionWired) return;
  details.dataset.mzfAccordionWired = "1";

  const summary = details.querySelector(SELECTORS.summary);
  const reveal = details.querySelector(SELECTORS.reveal);
  if (!summary || !reveal) return;

  summary.addEventListener("click", (event) => {
    // Leave it to the browser's instant toggle; CSS drops every transition too.
    // The click lands before the toggle, so a closed row here is about to open.
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      if (!details.open) {
        openSiblings(details).forEach((row) => {
          row.open = false;
        });
      }
      return;
    }

    event.preventDefault();
    if (details.classList.contains(CLASSES.collapsing)) return;

    if (details.open) {
      collapse(details, reveal);
    } else {
      openSiblings(details).forEach((row) => {
        const rowReveal = row.querySelector(SELECTORS.reveal);
        if (rowReveal) {
          collapse(row, rowReveal);
        } else {
          row.open = false;
        }
      });
      expand(details, reveal);
    }
  });
}

export function initAllAccordionBlocks() {
  document.querySelectorAll(SELECTORS.item).forEach(initAccordionItem);
}
