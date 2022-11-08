const RelatedArticles = {
  floatRelatedArticlesNextToThirdElement: () => {
    const firstParagraph = document.querySelector(
      ".paragraph-block .rich-text"
    );
    const relatedContainer = document.querySelector(
      "#buyersguide-related-content"
    );
    if (!firstParagraph || !relatedContainer) return;
    const relatedContent = relatedContainer.querySelector("div");
    const relatedPlace = firstParagraph.querySelector("*:nth-child(3)");
    if (!relatedPlace) return;
    firstParagraph.insertBefore(relatedContent, relatedPlace);
    relatedContent.classList.add(
      "large:tw-float-right",
      "tw-p-4",
      "tw-pr-0",
      "large:tw-mr-[-20%]"
    );
  },
};

export default RelatedArticles;
