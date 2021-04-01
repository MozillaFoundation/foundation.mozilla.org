/**
 * Checking whether the page has more than 5 items in the summary link section, if so, display them in a two column format.
 * If < 5 links, display them in one column
 */
export default () => {
  const summaryArticleSection = document.querySelector(".article-links");
  const countOfArticleLinks = document.querySelectorAll(".article-summary-link")
    .length;

  if (countOfArticleLinks > 5) {
    summaryArticleSection.classList.add("article-links__two-col");
  }
};
