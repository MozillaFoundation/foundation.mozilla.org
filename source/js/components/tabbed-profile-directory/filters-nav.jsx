import React from "react";

const FiltersNav = ({ filters, onFilterClick, currentFilterValue }) => {
  const isActiveButton = (filter, buttonIndex) => {
    // If current filter value is selected
    if (currentFilterValue === filter.filter_value) {
      return true;
    }
    // Select first button when there is no filter value.
    if (!currentFilterValue && buttonIndex === 0) {
      return true;
    }
    return false;
  };

  return (
    <div className="my-2">
      <nav
        aria-label="Profile Filters"
        className="tw-flex-row tw-mb-6 tw-w-full tw-flex"
      >
        <div className="tw-w-full" id="multipage-nav">
          {filters.map((filter, index) => (
            <button
              className={`multipage-link ${
                isActiveButton(filter, index) ? "active" : ""
              }`}
              onClick={(e) => {
                onFilterClick(filter);
              }}
              key={filter.filter_value}
            >
              {filter.filter_label}
            </button>
          ))}
        </div>
      </nav>
    </div>
  );
};

export default FiltersNav;
