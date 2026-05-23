/**
 * Forwards a click on a visible share button to its hidden ShareProgress anchor.
 * Buttons opt in by setting `data-sp-target="<id of ShareProgress wrapper>"`.
 *
 * Plain copy-to-clipboard behavior is handled separately by
 * `components/copy_to_clipboard.js`.
 */
function handleShareProgressClick(event) {
  const el = event.currentTarget;
  const shareProgressTarget = el.getAttribute("data-sp-target");
  if (!shareProgressTarget) return;

  const shareProgressButtonAnchor = document.querySelector(
    `#${shareProgressTarget} a`,
  );
  if (shareProgressButtonAnchor) {
    shareProgressButtonAnchor.click();
  }
}

export function initShareProgressButtons() {
  document.querySelectorAll("[data-sp-target]").forEach((button) => {
    button.addEventListener("click", handleShareProgressClick);
  });
}
