import React from "react";
import ReactDOM from "react-dom";
import TabbedProfileFilters from "../../components/tabbed-profile-directory/tabbed-profile-directory";

/**
 * Inject custom tabbed pulse profile filtering
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 */
export default (apps) => {
  const domContainers = document.querySelectorAll(
    "[data-tabbed-profile-filters-block]"
  );

  // Init Tabbed Profile Filters with properties
  domContainers.forEach((target) => {
    // Get options for filters
    const contentArea = target.querySelector(
      "[data-tabbed-profile-filters-content]"
    );
    let profiles;
    let filterOptions;
    let subFilters;
    try {
      profiles = JSON.parse(
        target.querySelector("#pulse-profiles").textContent
      );
      filterOptions = JSON.parse(
        target.querySelector("#pulse-profile-filter-options").textContent
      );
      subFilters = JSON.parse(
        target.querySelector("#pulse-profile-subfilters").textContent
      );
    } catch (err) {
      console.error(err);
    }

    apps.push(
      new Promise((resolve) => {
        ReactDOM.render(
          <TabbedProfileFilters
            apiEndPoint={contentArea.dataset.apiEndpoint}
            filterKey={contentArea.dataset.filterKey}
            filterOptions={filterOptions}
            subFilters={subFilters}
            subfiltersLabel={contentArea.dataset.subfiltersLabel}
            whenLoaded={() => resolve}
            profiles={profiles}
            // subFilters={subFilters}
          />,
          target
        );
      })
    );
  });
};
