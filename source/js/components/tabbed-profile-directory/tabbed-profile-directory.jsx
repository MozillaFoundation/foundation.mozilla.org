import React, {useEffect, useState} from 'react'
import PulseProfile from "../pulse-profile/pulse-profile";
import LoadingSpinner from "./loading-spinner";

const TabbedProfileFilters = ({
                                apiEndPoint,
                                filterKey,
                                filterOptions,
                                subFilters,
                                whenLoaded,
                              }) => {
  const filterOptionsList = JSON.parse(filterOptions).map((filterOption) => filterOption.fields)
  const [activeButton, setActiveButton] = useState(null);
  const [filteredProfiles, setFilteredProfiles] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentFilterValue, setCurrentFilterValue] = useState(null);

  // Component is loaded
  useEffect(() => {
    // This component has been loaded and resolve promise
    whenLoaded();
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

    // Make clicked button active
    setActiveButton(filterValue);

    // Retrieve api data
    const data = await getData(filterValue);

    // Set filtered profiles state
    setFilteredProfiles(data);
  };

  return (
    <div>
      <div className="my-2">
        <nav aria-label="Profile Filters" className="tw-flex-row tw-mb-6 tw-w-full tw-hidden medium:tw-flex tw-container">
          <div className="tw-w-full" id="multipage-nav">
            {filterOptionsList.map((filter) => (
              <button
                className={`multipage-link ${
                  activeButton === filter.filter_value ? "active" : ""
                }`}
                onClick={() => filterProfiles(filter.filter_value)}
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
        {loading && <LoadingSpinner />}

        {/* Done loading and profiles exist */}
        {filteredProfiles &&
        !loading &&
        filteredProfiles.map((profile) => <PulseProfile profile={profile}/>)}
      </div>
    </div>
  );
};

export default TabbedProfileFilters;
