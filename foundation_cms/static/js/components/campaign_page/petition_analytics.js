export function initPetitionAnalytics(root = document) {
  const campaign = root.querySelector("[data-petition-state]");
  if (!campaign) return;

  root.querySelectorAll("button[data-label]").forEach((button) => {
    button.addEventListener("click", () => {
      const label = button.getAttribute("data-label");
      const action =
        button.getAttribute("name") === "action" ? button.value : "click";

      if (typeof window.gtag === "function") {
        window.gtag("event", "petition_flow_button", {
          action,
          label,
          page_id: campaign.dataset.petitionPageId,
          state: campaign.dataset.petitionState,
        });
      }

      console.log(`Button clicked: ${label} (${action})`);
    });
  });
}
