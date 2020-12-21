/**
 * Summary bar on the publication page shows up when scrolled passed the hero.
 */
export default () => {
  console.log("555")
  const summaryBlock = document.querySelector(".article-navbar-container");
  const marginOffset = getComputedStyle(summaryBlock).getPropertyValue('--top-offset');
  const dropDownMenu = document.querySelector(".article-summary-menu");
  const articleSummaryToggle = document.querySelector(".article-summary-toggle");
  const hero = document.querySelector('.publication-hero-container');
  const nav = document.querySelector(".primary-nav-container");
  if (summaryBlock && hero && nav && dropDownMenu) {

    const total =
      hero.offsetHeight + nav.offsetHeight - summaryBlock.offsetHeight;

    window.addEventListener(
      "scroll",
      () => {
        if(window.scrollY > total) {
          // Toggle summary block off
          summaryBlock.style.top = "0";
          summaryBlock.setAttribute("aria-hidden", true);
        } else {
          // Toggle summary block on
          summaryBlock.style.top = marginOffset;
          summaryBlock.setAttribute("aria-hidden", false);
          dropDownMenu.classList.remove("d-block");
          articleSummaryToggle.classList.remove("show");
        }
      },
      {
        passive: true
      }
    );
  }};
