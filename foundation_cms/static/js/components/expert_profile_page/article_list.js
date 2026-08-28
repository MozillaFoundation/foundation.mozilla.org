const SELECTORS = {
  list: "[data-expert-profile-article-list]",
  item: ":scope > li",
  showMoreButton: "[data-expert-profile-show-articles]",
};

function hideOverflowArticles(articles, visibleArticleCount) {
  const hiddenArticles = articles.slice(visibleArticleCount);

  hiddenArticles.forEach((article) => {
    article.hidden = true;
  });

  return hiddenArticles;
}

function revealOverflowArticles(hiddenArticles, showMoreButton) {
  hiddenArticles.forEach((article) => {
    article.hidden = false;
  });
  showMoreButton.hidden = true;
}

export function initExpertProfileArticleList() {
  document.querySelectorAll(SELECTORS.list).forEach((articleList) => {
    const section = articleList.closest(".expert-profile-section--articles");
    const showMoreButton = section?.querySelector(SELECTORS.showMoreButton);

    if (!showMoreButton) return;

    const articles = Array.from(articleList.querySelectorAll(SELECTORS.item));
    const visibleArticleCount =
      Number.parseInt(articleList.dataset.visibleCount, 10) || articles.length;
    const hiddenArticles = hideOverflowArticles(articles, visibleArticleCount);

    if (!hiddenArticles.length) {
      showMoreButton.hidden = true;
      return;
    }

    showMoreButton.addEventListener("click", () => {
      revealOverflowArticles(hiddenArticles, showMoreButton);
    });
  });
}
