import setupSearchBar from "./search-bar";

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

  if (
    !location.pathname.includes("categories") &&
    !location.pathname.endsWith("/privacynotincluded/")
  ) {
    setupSearchBar(
      "#pni-mobile-bar",
      "#pni-mobile-container .clear-icon",
      `#pni-mobile-container`
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
