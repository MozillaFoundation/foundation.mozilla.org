import React from "react";
import { createRoot } from "react-dom/client";
import TabbedProfileFilters from "../../components/tabbed-profile-directory/tabbed-profile-directory";

/**
 * Inject custom tabbed pulse profile filtering
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
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
        const root = createRoot(target);
        root.render(
          <TabbedProfileFilters
            apiEndPoint={contentArea.dataset.apiEndpoint}
            filterKey={contentArea.dataset.filterKey}
            filterOptions={filterOptions}
            subFilters={subFilters}
            subfiltersLabel={contentArea.dataset.subfiltersLabel}
            subfiltersKey={contentArea.dataset.subfiltersKey}
            whenLoaded={() => resolve}
            profiles={profiles}
          />
        );
      })
    );
  });
};
