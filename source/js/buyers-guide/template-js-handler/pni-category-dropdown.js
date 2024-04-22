export default () => {
  const dropdown = document.querySelector(".pni-category-dropdown");
  const dropdownButton = dropdown.querySelector(
    ".pni-category-dropdown-button"
  );
  const dropdownButtonContent = dropdownButton.querySelector("span");
  const dropdownButtonChevron = dropdownButton.querySelector("svg");
  const dropdownSelect = dropdown.querySelector(
    "#pni-category-dropdown-select"
  );
  let defaultDropdownHeaderText; // Keep track of dropdown button's default text for different locales

  const navLinkMargin = 20; // Calculate which items go into the dropdown
  const categoryWrapper = document.querySelector("#pni-category-wrapper");
  const categoryNav = document.querySelector("#product-review");

  // Calculate width and margin
  const calculateWidthAndMargin = (ele) => ele.clientWidth + navLinkMargin;

  // Resize category navigation
  const resizeCategoryNavigation = () => {
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
  };

  // Add category to dropdown
  const addCategoryToDropdown = (category) => {
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
  };

  // Highlight selected category
  const highlightSelectedCategory = () => {
    const activeCategory = document.querySelector(
      "#pni-category-dropdown-select .active"
    );

    const dropdownHeaderText = dropdownButtonContent.querySelector("span");
    if (activeCategory) {
      dropdownHeaderText.innerText = activeCategory.innerText;
      dropdownHeaderText.classList.add("tw-text-black");
      dropdownHeaderText.setAttribute("aria-current", "page");
    } else {
      dropdownHeaderText.innerText = defaultDropdownHeaderText;
      dropdownHeaderText.classList.remove("tw-text-black");
      dropdownHeaderText.removeAttribute("aria-current");
    }
  };

  // Open menu
  const openMenu = (withFocus = false) => {
    dropdownSelect.classList.remove("tw-hidden");
    dropdownButton.setAttribute("aria-expanded", "true");
    dropdownButtonChevron.classList.add("tw-stroke-black", "tw-rotate-180");

    if (withFocus) {
      const firstOption = dropdownSelect.querySelector("li > a");
      if (firstOption) {
        firstOption.focus();
      }
    }
  };

  // Close menu
  const closeMenu = () => {
    dropdownSelect.classList.add("tw-hidden");
    dropdownButton.setAttribute("aria-expanded", "false");
    dropdownButtonChevron.classList.remove("tw-stroke-black", "tw-rotate-180");
  };

  if (dropdown && dropdownButton && dropdownSelect) {
    // removing styling that are exclusively used when JS is disabled or before it is loaded
    dropdown.classList.add("tw-block");
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

    defaultDropdownHeaderText =
      dropdownButtonContent.querySelector("span").innerText;

    // If there is an overflow of categories lets start moving them to the category dropdown
    if (categoryWrapper.clientWidth > categoryNav.clientWidth) {
      resizeCategoryNavigation();
      highlightSelectedCategory();
    }

    // Detect class changes within links
    new MutationObserver(() => {
      highlightSelectedCategory();
    }).observe(dropdownSelect, {
      childList: true,
      subtree: true,
      attributes: true,
    });

    // Support adjusting screen size (avoid having to refresh the page)
    window.onresize = function () {
      if (categoryWrapper.clientWidth > categoryNav.clientWidth) {
        resizeCategoryNavigation();
        highlightSelectedCategory();
      }
    };

    // Event listener for keyboard events on dropdown button
    dropdownButton.addEventListener("keydown", function (event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        if (dropdownButton.getAttribute("aria-expanded") === "false") {
          openMenu(true);
        } else {
          closeMenu();
        }
      }

      if (event.key === "ArrowDown") {
        if (dropdownButton.getAttribute("aria-expanded") === "true") {
          event.preventDefault();
          const firstOption = dropdownSelect.querySelector("li > a");
          if (firstOption) {
            firstOption.focus();
          }
        } else {
          openMenu(true);
        }
      }
    });

    // Event listener for click events on dropdown button
    dropdownButton.addEventListener("click", function (event) {
      event.stopPropagation();
      if (dropdownButton.getAttribute("aria-expanded") === "false") {
        openMenu();
      } else {
        closeMenu();
      }
    });

    // Event listener for keyboard events on dropdown container
    dropdownSelect.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeMenu();
      }
    });

    // Event listener for keyboard and click events on dropdown options
    dropdownSelect.querySelectorAll("li").forEach(function (option) {
      // Event listener for click events on dropdown options
      option.querySelector("a")?.addEventListener("click", function () {
        closeMenu();
      });

      // Event listener for keyboard events on dropdown options
      option.addEventListener("keydown", function (event) {
        if (event.key === " " || event.key === "Enter") {
          event.preventDefault();
          option.querySelector("a").click();
          closeMenu();
        }

        if (event.key === "ArrowDown") {
          event.preventDefault();
          const nextOption = option?.nextElementSibling?.querySelector("a");
          if (nextOption) {
            nextOption.focus();
          }
        } else if (event.key === "ArrowUp") {
          event.preventDefault();
          const prevOption = option?.previousElementSibling?.querySelector("a");
          if (prevOption) {
            prevOption.focus();
          } else {
            dropdownButton.focus();
          }
        }
      });
    });
  }
};
