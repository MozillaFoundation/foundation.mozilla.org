/**
 * Newsletter box is hidden by default.
 * Make newsletter box visible again for JS-enabled browser users
 * so they can interact with the newsletter box.
 */
const NewsletterBox = {
  toggleVisibilityClasses: () => {
    const buyersGuideNewsletterBox = document.querySelectorAll(
      ".buyersguide-newsletter-box"
    );
    // Used for toggle visibility for buyersguide newsletter container
    if (buyersGuideNewsletterBox.length > 0) {
      buyersGuideNewsletterBox.forEach((box) =>
        box.classList.remove("tw-hidden")
      );
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
