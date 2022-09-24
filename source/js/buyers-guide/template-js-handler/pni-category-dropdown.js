export default () => {
  const dropdown = document.querySelector(".pni-category-dropdown");
  const dropdownSelect = document.querySelector(
    ".pni-category-dropdown-select"
  );
  const dropdownSelectItems = document.querySelectorAll(
    ".pni-category-dropdown-select > li, .pni-category-dropdown-select > li > a"
  );

  if (dropdown) {
    dropdown.addEventListener("click", function (event) {
      event.stopPropagation();
      dropdownSelect.classList.remove("tw-hidden");
    });
    dropdownSelectItems.forEach((item) => {
      item.addEventListener("click", function (event) {
        event.stopPropagation();
        dropdownSelect.classList.add("tw-hidden");
      });
    });
  }
};
