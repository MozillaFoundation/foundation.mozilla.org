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
    const filterOptions = JSON.parse(
      target.querySelector(
        "[data-pulse-profile-filter-options] #pulse-profile-filter-options"
      ).textContent
    );
    // const subFilters = JSON.parse(document.getElementById('pulse-profile-subfilters').textContent)

    apps.push(
      new Promise((resolve) => {
        ReactDOM.render(
          <TabbedProfileFilters
            apiEndPoint={contentArea.dataset.apiEndpoint}
            filterKey={contentArea.dataset.filterKey}
            filterOptions={filterOptions}
            whenLoaded={() => resolve}
            // subFilters={subFilters}
          />,
          target
        );
      })
    );
  });
};
