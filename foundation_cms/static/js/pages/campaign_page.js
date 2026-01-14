const SELECTORS = {
  comfirmationBanner: ".confirmation-notice-banner",
  comfirmationBannerCloseButton:
    ".confirmation-notice-banner [data-banner-close-button]",
  shareButtons:
    ".petition__share-button-wrapper button, .petition__share-button-wrapper a",
  formThankYouUrlField: ".petition__form-wrapper #tfa_500",
  formNewsletterCheckbox: ".petition__form-wrapper #tfa_495",
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

const newsletterCheckbox = document.querySelector(
  SELECTORS.formNewsletterCheckbox,
);
const formThankYouUrlField = document.querySelector(
  SELECTORS.formThankYouUrlField,
);

if (newsletterCheckbox && formThankYouUrlField) {
  newsletterCheckbox.addEventListener("change", (e) => {
    const baseUrl = new URL(formThankYouUrlField.value);

    if (e.target.checked) {
      baseUrl.searchParams.set("newsletter_optin", "true");
    } else {
      baseUrl.searchParams.delete("newsletter_optin");
    }

    formThankYouUrlField.value = baseUrl.toString();
  });
}
