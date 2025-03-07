export default (inputSelector, clearSelector, searchSelector) => {
  const input = document.querySelector(inputSelector);
  const clearIcon = document.querySelector(clearSelector);
  const searchBar = document.querySelector(searchSelector);

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
