const NewsletterBox = {
  toggleVisibilityClasses: () => {
    const buyersGuideNewsletterBox = document.querySelector(
      "#buyersguide-newsletter-box"
    );
    // Used for toggle visibility for buyersguide newsletter container
    if (buyersGuideNewsletterBox) {
      buyersGuideNewsletterBox.classList.remove("tw-hidden");
    }

    // Used for buyersguide product review grid toggle visibility
    const buyersGuideGridContainer = document.querySelector(
      "#product-grid-newsletter-signup"
    );
    if (buyersGuideGridContainer) {
      buyersGuideGridContainer.classList.add("tw-flex");
      buyersGuideGridContainer.classList.remove("tw-hidden");
    }
  },
};

export default NewsletterBox;
