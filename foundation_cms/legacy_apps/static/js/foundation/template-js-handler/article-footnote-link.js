/**
 * Attach click handler to article page's footnote links,
 * taking stikcy navs into account,
 * so the anchor target can be properly scrolled into view
 */
export default () => {
  const links = document.querySelectorAll("#view-article a.footnote-number");
  const siteNav = document.querySelector(".primary-nav-container");
  const summaryNav = document.querySelector(".article-navbar");

  if (!(links && siteNav && summaryNav)) return;

  links.forEach((link) => {
    link.addEventListener(`click`, (event) => {
      event.preventDefault();

      const target = document.querySelector(link.getAttribute(`href`));
      const offset = siteNav.scrollHeight + summaryNav.scrollHeight;
      const top =
        target.getBoundingClientRect().top + window.pageYOffset - offset;

      window.scrollTo({
        top: top,
        behavior: `smooth`,
      });
    });
  });
};
