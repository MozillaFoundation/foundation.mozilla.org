export default () => {
  if (
    location.pathname.includes("categories") ||
    location.pathname.endsWith("/privacynotincluded/")
  )
    return;

  const input = document.querySelector("#product-filter-search-input");
  const clearIcon = document.querySelector(
    "#product-filter-search-input + .clear-icon"
  );
  const searchBar = document.querySelector(`#product-filter-search`);

  if (!input || !clearIcon || !searchBar) return;

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
};
