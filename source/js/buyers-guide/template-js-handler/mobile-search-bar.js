export default () => {
  const mobileSearch = document.querySelector("#mobile-search");

  if (!mobileSearch) return;

  mobileSearch.addEventListener("click", function () {
    const searchContainer = document.querySelector("#pni-mobile-container");

    if (!searchContainer) return;

    searchContainer.classList.toggle("tw-hidden");

    // TODO Finish search bar implementation
  });
};
