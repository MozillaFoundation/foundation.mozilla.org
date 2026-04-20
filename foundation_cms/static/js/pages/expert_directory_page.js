document.addEventListener("click", (e) => {
  const btn = e.target.closest(".expert-card__topics-toggle");
  if (!btn) return;

  const topicsContainer = btn.closest(".expert-card__topics");
  if (!topicsContainer) return;

  const expanded = topicsContainer.classList.toggle(
    "expert-card__topics--expanded",
  );
  btn.setAttribute("aria-expanded", String(expanded));
  btn.setAttribute(
    "aria-label",
    expanded ? btn.dataset.labelCollapse : btn.dataset.labelExpand,
  );
});
