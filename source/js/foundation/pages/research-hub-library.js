function main() {
  initializeJS();
}

function initializeJS() {
  // Hide the filter section and apply the mobile modal styles
  const filterSection = document.getElementById("filter");
  filterSection.classList.add("tw-hidden");
  filterSection.classList.add("rh-filter-modal");
  filterSection.classList.remove("tw-pt-7");

  // Replace jump link with open button
  const filterJumpLink = document.getElementById("filter-section-jump-link");
  filterJumpLink.classList.add("tw-hidden");
  const filterShowButton = document.getElementById(
    "filter-section-show-button"
  );
  filterShowButton.classList.remove("tw-hidden");

  filterShowButton.addEventListener("click", showFilterModal);
  const filterHideButton = document.getElementById(
    "filter-section-hide-button"
  );
  filterHideButton.classList.remove("tw-hidden");
  filterHideButton.addEventListener("click", hideFilterModal);

  const sortSelect = document.getElementById("sort-select");
  sortSelect.addEventListener("change", updateSearchForm);
}

function showFilterModal(event) {
  const filterSection = document.getElementById("filter");
  filterSection.classList.remove("tw-hidden");
}

function hideFilterModal(event) {
  const filterSection = document.getElementById("filter");
  filterSection.classList.add("tw-hidden");
}

function updateSearchForm(event) {
  const searchForm = document.getElementById("search-form");
  searchForm.submit();
}

main();
