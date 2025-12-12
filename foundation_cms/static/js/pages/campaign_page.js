const SELECTORS = {
  comfirmationBanner: ".confirmation-notice-banner",
  comfirmationBannerCloseButton:
    ".confirmation-notice-banner [data-banner-close-button]",
};

const banner = document.querySelector(SELECTORS.comfirmationBanner);
const bannerCloseButton = document.querySelector(
  SELECTORS.comfirmationBannerCloseButton,
);

console.log(banner, bannerCloseButton);

if (banner && bannerCloseButton) {
  bannerCloseButton.addEventListener("click", (e) => {
    e.preventDefault();

    banner.remove();
  });
}
