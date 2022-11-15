import setupSearchBar from "./search-bar";

export default () => {
  if (
    location.pathname.includes("categories") ||
    location.pathname.endsWith("/privacynotincluded/")
  )
    return;

  setupSearchBar(
    "#product-filter-search-input",
    "#product-filter-search-input + .clear-icon",
    `#product-filter-search`
  );
};
