const RelatedArticles = {
  floatRelatedArticlesNextToThirdElement: () => {
    const firstParagraph = document.querySelector(
      ".paragraph-block .rich-text"
    );
    const relatedContainer = document.querySelector(
      "#article-primary-related-articles"
    );
    if (!firstParagraph || !relatedContainer) return;
    const relatedContent = relatedContainer.querySelector("div");
    /*
     * if there is at least 3 children inside the rich body container.
     * Usually there is a header(h1-6) and a few paragraphs blocks to start most articles.
     * If we do not have at least that many elements we leave the related articles at the bottom of the article page
     */
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
