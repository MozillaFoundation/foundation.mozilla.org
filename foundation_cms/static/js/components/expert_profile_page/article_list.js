const SELECTORS = {
  list: "[data-expert-profile-article-list]",
  item: ".listing-content__item",
  showMoreButton: "[data-expert-profile-show-articles]",
};

const VISIBLE_ARTICLE_COUNT = 3;

/**
 * Hides article items after the initial visible count.
 *
 * @param {HTMLElement[]} articles - Article list items in render order.
 * @returns {HTMLElement[]} Items hidden behind the show-more button.
 */
function hideOverflowArticles(articles) {
  const hiddenArticles = articles.slice(VISIBLE_ARTICLE_COUNT);

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
  const hiddenArticles = hideOverflowArticles(articles);

  if (!hiddenArticles.length) {
    showMoreButton.hidden = true;
    return;
  }

  showMoreButton.addEventListener("click", () => {
    revealOverflowArticles(hiddenArticles, showMoreButton);
  });
}
