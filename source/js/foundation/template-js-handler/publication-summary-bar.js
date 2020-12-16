/**
 * Summary bar on the publication page shows up when scrolled passed the hero.
 */
export default () => {
  const summaryBar = document.querySelector(".article-navbar");
  const marginOffset = getComputedStyle(summaryBar).getPropertyValue('--margin-top');
  const dropDownMenu = document.querySelector(".article-summary-menu");
  if(summaryBar) {
    const heroHeight = document.querySelector('.publication-hero-container').offsetHeight;
    const navHeight = document.querySelector(".primary-nav-container").offsetHeight;
    const total = heroHeight + navHeight - summaryBar.offsetHeight;
    window.addEventListener("scroll", () => {
      if(window.scrollY > total) {
        summaryBar.style.marginTop = "0";
      } else{
        summaryBar.style.marginTop = marginOffset;
        dropDownMenu.classList.remove("d-block");
      }
    });
  }};
