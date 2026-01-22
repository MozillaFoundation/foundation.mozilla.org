const SELECTORS = {
  comfirmationBanner: ".confirmation-notice-banner",
  comfirmationBannerCloseButton:
    ".confirmation-notice-banner [data-banner-close-button]",
};

/**
 * Initializes the confirmation notice banner functionality.
 * Sets up event listener on the close button to remove the banner when clicked.
 */
export function initConfirmationNoticeBanner() {
  const banner = document.querySelector(SELECTORS.comfirmationBanner);
  const bannerCloseButton = document.querySelector(
    SELECTORS.comfirmationBannerCloseButton,
  );

  if (banner && bannerCloseButton) {
    bannerCloseButton.addEventListener("click", (e) => {
      e.preventDefault();
      banner.remove();
    });
  }
}
