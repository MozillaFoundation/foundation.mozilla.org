const SELECTORS = {
  lightbox: "dialog.donate-lightbox",
  closeButton: "[data-donate-lightbox-close-button]",
  ctaButton: "[data-donate-banner-cta-button]",
};

function openLightbox(lightbox) {
  lightbox.showModal();
}

export function initDonateLightbox() {
  const lightbox = document.querySelector(SELECTORS.lightbox);
  if (!lightbox) return;

  const closeButton = lightbox.querySelector(SELECTORS.closeButton);
  closeButton?.addEventListener("click", () => lightbox.close());

  // close on click outside the modal
  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) lightbox.close();
  });

  if (window.wagtailAbTesting) {
    const ctaButton = lightbox.querySelector(SELECTORS.ctaButton);
    ctaButton?.addEventListener("click", () => {
      wagtailAbTesting.triggerEvent("donate-banner-link-click");
    });
  }

  openLightbox(lightbox);
}
