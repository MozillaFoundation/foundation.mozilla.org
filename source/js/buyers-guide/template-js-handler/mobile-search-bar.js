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
    const input = document.querySelector("#pni-mobile-bar");
    const clearIcon = document.querySelector(
      "#pni-mobile-container .clear-icon"
    );

    clearIcon.addEventListener("click", function () {
      searchContainer.classList.remove(`has-content`);
      input.value = "";
    });

    input.addEventListener(`input`, function () {
      const searchText = input.value.trim();

      if (searchText) {
        searchContainer.classList.add(`has-content`);
      } else {
        searchContainer.classList.remove(`has-content`);
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
  }
};
