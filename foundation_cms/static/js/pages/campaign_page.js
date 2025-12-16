const SELECTORS = {
  comfirmationBanner: ".confirmation-notice-banner",
  comfirmationBannerCloseButton:
    ".confirmation-notice-banner [data-banner-close-button]",
  shareButtons:
    ".petition__share-button-wrapper button, .petition__share-button-wrapper a",
};

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

function shareButtonClicked(event) {
  const el = event.currentTarget;
  const shareProgressTarget = el.getAttribute("data-sp-target");

  if (shareProgressTarget) {
    const shareProgressButtonAnchor = document.querySelector(
      `#${shareProgressTarget} a`,
    );
    if (shareProgressButtonAnchor) {
      shareProgressButtonAnchor.click();
    }
  } else {
    const url = window.location.href.split("?")[0].split("#")[0];
    navigator.clipboard.writeText(url);
    el.innerText = "Copied";
  }
}

const shareButtons = document.querySelectorAll(SELECTORS.shareButtons);
shareButtons.forEach((shareButton) => {
  shareButton.addEventListener("click", (e) => {
    e.preventDefault();
    shareButtonClicked(e);
  });
});
