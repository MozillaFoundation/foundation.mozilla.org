export function initPillarCardLinks() {
  document
    .querySelectorAll(".pillar-card-set__card[data-href]")
    .forEach((card) => {
      card.style.cursor = "pointer";
      card.addEventListener("click", function (e) {
        // prevent double navigation (link click bubbles up to card)
        if (e.target.closest(".pillar-card-set__card-link")) return;

        const href = this.dataset.href;
        const target = this.dataset.target;

        if (target === "_blank") {
          window.open(href, "_blank", "noopener,noreferrer");
        } else {
          window.location.href = href;
        }
      });
    });
}
