const SELECTORS = {
  list: "[data-expert-profile-article-list]",
  item: ".listing-content__item",
  showMoreButton: "[data-expert-profile-show-articles]",
};

/**
 * Hides article items after the initial visible count.
 *
 * @param {HTMLElement[]} articles - Article list items in render order.
 * @param {number} visibleArticleCount - Number of articles visible before expansion.
 * @returns {HTMLElement[]} Items hidden behind the show-more button.
 */
function hideOverflowArticles(articles, visibleArticleCount) {
  const hiddenArticles = articles.slice(visibleArticleCount);

  hiddenArticles.forEach((article) => {
    article.hidden = true;
  });

  return hiddenArticles;
}

/**
 * Reveals all overflow article items and hides the trigger button.
 *
 * @param {HTMLElement[]} hiddenArticles - Article items hidden on load.
 * @param {HTMLButtonElement} showMoreButton - Button that reveals the hidden articles.
 * @returns {void}
 */
function revealOverflowArticles(hiddenArticles, showMoreButton) {
  hiddenArticles.forEach((article) => {
    article.hidden = false;
  });
  showMoreButton.hidden = true;
}

/**
 * Initializes the Expert Profile article show-more behavior.
 *
 * @returns {void}
 */
export function initExpertProfileArticleList() {
  const articleList = document.querySelector(SELECTORS.list);
  const showMoreButton = document.querySelector(SELECTORS.showMoreButton);

  if (!articleList || !showMoreButton) return;

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
}
