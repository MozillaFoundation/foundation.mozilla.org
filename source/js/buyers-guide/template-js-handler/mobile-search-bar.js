export default () => {
  const mobileSearch = document.querySelector("#mobile-search");
  const searchContainer = document.querySelector("#pni-mobile-container");

  if (!mobileSearch) return;

  mobileSearch.addEventListener("click", function () {
    const burger = document.querySelector(".burger");

    if (!searchContainer) return;

    if (burger && burger.classList.contains("menu-open")) {
      document.querySelector(".burger").click();
    }
    searchContainer.classList.toggle("tw-hidden");
  });

  /**
   * if the user is not on the product review pages,
   * the search bar has a different behavior that redirects to product review
   */

  if (
    !location.pathname.includes("categories") &&
    !location.pathname.endsWith("/privacynotincluded/")
  ) {
    const mobileInput = document.querySelector("#pni-mobile-bar");
    const mobileClearIcon = document.querySelector(
      "#pni-mobile-container .clear-icon"
    );

    mobileClearIcon.addEventListener("click", function () {
      searchContainer.classList.remove(`has-content`);
      mobileInput.value = "";
    });

    mobileInput.addEventListener(`input`, function () {
      const searchText = mobileInput.value.trim();

      if (searchText) {
        searchContainer.classList.add(`has-content`);
      } else {
        searchContainer.classList.remove(`has-content`);
      }
    });

    mobileInput.addEventListener("keypress", function (event) {
      // If the user presses the "Enter" key on the keyboard or mobile
      if (event.key === "Enter" && mobileInput.value) {
        event.preventDefault();
        const url = new URL("/privacynotincluded/", location.href);
        url.searchParams.set("search", mobileInput.value);
        url.search = url.searchParams.toString();
        url.hash = "product-review";
        location.href = url.toString();
      }
    });

    const input = document.querySelector("#product-filter-search-input");
    const clearIcon = document.querySelector(
      "#product-filter-search-input + .clear-icon"
    );
    const searchBar = document.querySelector(`#product-filter-search`);

    clearIcon.addEventListener("click", function () {
      searchBar.classList.remove(`has-content`);
      input.value = "";
    });

    input.addEventListener(`input`, function () {
      const searchText = input.value.trim();

      if (searchText) {
        searchBar.classList.add(`has-content`);
      } else {
        searchBar.classList.remove(`has-content`);
      }
    });

    input.addEventListener("keypress", function (event) {
      // If the user presses the "Enter" key on the keyboard or mobile
      if (event.key === "Enter" && input.value) {
        event.preventDefault();
        const url = new URL("/privacynotincluded/", location.href);
        url.searchParams.set("search", input.value);
        url.search = url.searchParams.toString();
        url.hash = "product-review";
        location.href = url.toString();
      }
    });
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
