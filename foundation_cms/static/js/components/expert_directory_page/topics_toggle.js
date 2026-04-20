const SELECTORS = {
  toggle: ".expert-card__topics-toggle",
  container: ".expert-card__topics",
};

export function initTopicsToggle() {
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(SELECTORS.toggle);
    if (!btn) return;

    const topicsContainer = btn.closest(SELECTORS.container);
    if (!topicsContainer) return;

    const expanded = topicsContainer.classList.toggle(
      "expert-card__topics--expanded",
    );
    btn.setAttribute("aria-expanded", `${expanded}`);
    btn.setAttribute(
      "aria-label",
      expanded ? btn.dataset.labelCollapse : btn.dataset.labelExpand,
    );
  });
}
