const articleList = document.querySelector(
  "[data-expert-profile-article-list]",
);
const showArticlesButton = document.querySelector(
  "[data-expert-profile-show-articles]",
);

if (articleList && showArticlesButton) {
  const visibleArticleCount = 3;
  const articles = Array.from(
    articleList.querySelectorAll(".listing-content__item"),
  );
  const hiddenArticles = articles.slice(visibleArticleCount);

  hiddenArticles.forEach((article) => {
    article.hidden = true;
  });

  if (!hiddenArticles.length) {
    showArticlesButton.hidden = true;
  }

  showArticlesButton.addEventListener("click", () => {
    hiddenArticles.forEach((article) => {
      article.hidden = false;
    });
    showArticlesButton.hidden = true;
  });
}
