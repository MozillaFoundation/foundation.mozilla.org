import React, {useEffect, useState, useRef} from "react";
import PulseProfile from "../pulse-profile/pulse-profile";
import LoadingSpinner from "./loading-spinner";
import { getText } from "./locales";

const TabbedProfileFilters = ({
                                apiEndPoint,
                                filterKey,
                                filterOptions,
                                subFilters,
                                whenLoaded,
                                profiles,
                              }) => {
  const filterOptionsList = JSON.parse(filterOptions).map(
    (filterOption) => filterOption.fields
  );
  const [filteredProfiles, setFilteredProfiles] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentFilterValue, setCurrentFilterValue] = useState(null);

  // Component is loaded
  useEffect(() => {
    // This component has been loaded and resolve promise
    whenLoaded();
    setLoading(false);

    if (profiles) {
      setFilteredProfiles(profiles);
    }

    // make sure that "back" does the right thing.
    window.addEventListener("popstate", (evt) => {
      const state = evt.state;
      if (!state) {
        return;
      }
      filterProfiles(state.type);
    });

  }, []);

  /**
   * After initial page load, the filter buttons are responsible for
   * fetching results "per filter entry".
   */
  const getData = (filterValue) => {
    if (!filterKey || !filterValue) {
      return;
    }

    // Set loading
    setLoading(true);

    // build and append the query arguments
    const query = `${filterKey}=${filterValue}`;

    // Perform our API call using the Fetch API
    return (
      fetch(`${apiEndPoint}&${query}`)
        // convert the resonse from JSON to real data
        .then((response) => {
          setLoading(false);
          return response.json();
        })
        .catch((error) => {
          setLoading(false);
          return error;
        })
    );
  };

  const filterProfiles = async (filterValue) => {
    // Do nothing if already filtered by this value
    if (filterValue === currentFilterValue) {
      return;
    }

    // Hold current filter value
    setCurrentFilterValue(filterValue);

    // Retrieve api data
    const data = await getData(filterValue);

    // Set filtered profiles state
    if (data) {
      setFilteredProfiles(data);
    }

    history.pushState({type: filterValue}, document.title);
    document.dispatchEvent(new CustomEvent("profiles:list-updated"));
  };

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
  }

  return (
    <div>
      <div className="my-2">
        <nav
          aria-label="Profile Filters"
          className="tw-flex-row tw-mb-6 tw-w-full tw-flex"
        >
          <div className="tw-w-full" id="multipage-nav">
            {filterOptionsList.map((filter, index) => (
              <button
                className={`multipage-link ${
                  isActiveButton(filter, index) ? "active" : ""
                }`}
                onClick={(e) => filterProfiles(filter.filter_value, e.target)}
                key={filter.filter_value}
              >
                {filter.filter_label}
              </button>
            ))}
          </div>
        </nav>
      </div>

      <div>
        {/* Loading */}
        {loading && <LoadingSpinner/>}

        {/* Done loading and profiles exist */}
        {filteredProfiles && filteredProfiles.length > 1 &&
        !loading &&
        <div className="tw-grid large:tw-grid-cols-2 tw-mb-5 w-full tw-gap-6">
          {filteredProfiles.map((profile) => (
            <PulseProfile key={profile.id} profile={profile}/>
          ))}
        </div>
        }

        {/* No Profiles from fetch */}
        {filteredProfiles && filteredProfiles.length < 1 && !loading && (
          <div>
            <p>{getText("No Profiles")}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TabbedProfileFilters;
