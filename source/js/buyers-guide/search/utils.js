export class Utils {
  static clearCategories() {
    if (document.querySelector(`#multipage-nav a.active`)) {
      document
        .querySelector(`#multipage-nav a.active`)
        .classList.remove(`active`);
      document
        .querySelector(`#multipage-nav a[data-name="None"]`)
        .classList.add(`active`);
    }

    if (document.querySelector(`#pni-nav-mobile a.active`)) {
      document
        .querySelector(`#pni-nav-mobile a.active`)
        .classList.remove(`active`);
      document
        .querySelector(`#pni-nav-mobile a[data-name="None"]`)
        .classList.add(`active`);
    }
  }
}
