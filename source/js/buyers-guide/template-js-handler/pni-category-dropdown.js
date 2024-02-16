// TODO Refactor to ES6 Class in future to match other components and include aria/keyboard shortcuts

export default () => {
  const dropdown = document.querySelector(".pni-category-dropdown");

  // Need this to keep track of the default text of the dropdown button when using different locales
  let defaultDropdownHeaderText;

  // Needed for calculating which items go into the dropdown
  const navLinkMargin = 20;
  const categoryWrapper = document.querySelector("#pni-category-wrapper");
  const categoryNav = document.querySelector("#product-review");

  const calculateWidthAndMargin = (ele) => ele.clientWidth + navLinkMargin;

  const dropdownSelect = document.querySelector(
    "#pni-category-dropdown-select"
  );
  const dropdownSelectItems = document.querySelectorAll(
    "#pni-category-dropdown-select > li, #pni-category-dropdown-select > li > a"
  );

  function resizeCategoryNavigation() {
    const categoryLinks = [
      ...document.querySelectorAll(
        "#buyersguide-category-link-container > .multipage-link"
      ),
    ].reverse();

    let linksForDropdown = [];

    const calculateLinksWidth = (links) =>
      links.reduce((acc, cur) => {
        return acc + calculateWidthAndMargin(cur);
      }, 0);

    for (const link of categoryLinks) {
      if (
        categoryWrapper.clientWidth - calculateLinksWidth(linksForDropdown) <
        categoryNav.clientWidth
      ) {
        break;
      }
      linksForDropdown.unshift(link);
    }

    linksForDropdown.forEach((e) => addCategoryToDropdown(e));
  }

  function addCategoryToDropdown(category) {
    const el = document.createElement("li");
    el.classList.add(
      "tw-bg-white",
      "tw-text-gray-40",
      "hover:tw-text-black",
      "tw-mb-0"
    );
    category.classList.add(
      "tw-w-full",
      "tw-mr-0",
      "tw-font-sans",
      "tw-font-bold",
      "tw-p-8",
      "tw-text-right"
    );
    category.classList.remove("tw-block");
    el.append(category);
    dropdownSelect.append(el);
  }

  function highlightSelectedCategory() {
    const activeCategory = document.querySelector(
      "#pni-category-dropdown-select .active"
    );

    const dropdownHeaderText = document.querySelector(
      ".pni-category-dropdown > span"
    );

    if (activeCategory) {
      dropdownHeaderText.innerText = activeCategory.innerText;
      dropdownHeaderText.classList.add("tw-text-black");
    } else {
      dropdownHeaderText.innerText = defaultDropdownHeaderText;
      dropdownHeaderText.classList.remove("tw-text-black");
    }
  }

  if (dropdown) {
    // removing styling that are exclusive used when JS is disabled or before it is loaded
    dropdown.classList.add("tw-inline-flex");
    dropdown.classList.remove("tw-hidden");
    categoryWrapper.classList.add("tw-w-max", "tw-min-w-full");
    document
      .querySelector("#buyersguide-category-link-container")
      .classList.remove(
        "tw-w-full",
        "large:tw-w-4/5",
        "tw-overflow-x-auto",
        "tw-mr-8"
      );

    defaultDropdownHeaderText = document.querySelector(
      ".pni-category-dropdown > span"
    ).innerText;

    // If there is an overflow of categories lets start moving them to the category dropdown
    if (categoryWrapper.clientWidth > categoryNav.clientWidth) {
      resizeCategoryNavigation();
      highlightSelectedCategory();
    }

    // Using to detect classes changes within the links
    new MutationObserver(() => {
      highlightSelectedCategory();
    }).observe(dropdownSelect, {
      childList: true,
      subtree: true,
      attributes: true,
    });

    // So people can test going to smaller screen sizes without having to refresh the page
    window.onresize = function () {
      if (categoryWrapper.clientWidth > categoryNav.clientWidth) {
        resizeCategoryNavigation();
        highlightSelectedCategory();
      }
    };

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
