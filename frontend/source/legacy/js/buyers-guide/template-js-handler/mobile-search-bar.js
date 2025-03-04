import setupSearchBar from "./search-bar";

export default () => {
  const mobileSearch = document.querySelector("#mobile-search");
  const searchContainer = document.querySelector(
    "#pni-mobile-search-container"
  );
  const mobileCatNav = document.querySelector("#pni-mobile-category-nav");

  if (!mobileSearch) return;

  mobileSearch.addEventListener("click", function () {
    const burger = document.querySelector(".burger");

    if (!searchContainer || !mobileCatNav) return;

    if (burger && burger.classList.contains("menu-open")) {
      document.querySelector(".burger").click();
    }

    // if the search bar is open, clear the search bar
    if (!searchContainer.classList.contains("tw-hidden")) {
      searchContainer.querySelector(`.clear-icon`).click();
    }

    searchContainer.classList.toggle("tw-hidden");
    mobileCatNav.classList.toggle("tw-hidden");
  });

  if (
    !location.pathname.includes("categories") &&
    !location.pathname.endsWith("/privacynotincluded/")
  ) {
    setupSearchBar(
      "#pni-mobile-bar",
      "#pni-mobile-search-container .clear-icon",
      `#pni-mobile-search-container`
    );
  } else {
    const input = document.querySelector("#pni-mobile-bar");

    input.addEventListener("keypress", function (event) {
      if (event.key === "Enter" && input.value) {
        event.preventDefault();
        const editorialContent = document.querySelector(".editorial-content");
        const navLinks = document.querySelectorAll(`.product-review-link`);
        for (const nav of navLinks) {
          nav.classList.add("active");
        }
        location.hash = "product-review";
        editorialContent.classList.add("tw-hidden");
        window.scrollTo(0, 0);
      }
    });
  }
};
