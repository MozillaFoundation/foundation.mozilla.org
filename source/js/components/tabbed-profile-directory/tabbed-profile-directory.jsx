import React, { useEffect, useState, useRef } from "react";
import PulseProfile from "../pulse-profile/pulse-profile";
import LoadingSpinner from "./loading-spinner";
import { getText } from "./locales";

const TabbedProfileFilters = ({
  apiEndPoint,
  filterKey,
  filterOptions,
  subFilters,
  subfiltersLabel,
  subfiltersKey,
  whenLoaded,
  profiles,
}) => {
  const filterOptionsList = JSON.parse(filterOptions).map(
    (filterOption) => filterOption.fields
  );
  const subfilterOptionsList = JSON.parse(subFilters).map((option) => ({
    ...option.fields,
  }));
  const [filteredProfiles, setFilteredProfiles] = useState(null);
  const [subFilteredProfiles, setSubFilteredProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentFilterValue, setCurrentFilterValue] = useState(null);

  const [selectedSubfilters, setSelectedSubfilters] = useState({});
  const [showAllSubFilteredItems, setShowAllSubFilteredItems] = useState(null);
  const [showSubfilters, setShowSubfilters] = useState(false);
  const [subFiltersExpanded, setSubFiltersExpanded] = useState(false);
  const subFiltersDropdown = useRef();

  // Component is loaded
  useEffect(() => {
    // This component has been loaded and resolve promise
    whenLoaded();
    setLoading(false);

    if (profiles) {
      setFilteredProfiles(profiles);
    }
  }, []);

  // Fetch data based on filter value
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
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (!subFiltersDropdown.current.contains(event.target)) {
        setSubFiltersExpanded(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
  }, [subFiltersDropdown]);

  // Close subFilters with escape
  useEffect(() => {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        setSubFiltersExpanded(false);
      }
    });
  }, []);

  const handleSelectSubfilter = (event) => {
    setSelectedSubfilters({
      ...selectedSubfilters,
      [event.target.name]: event.target.checked,
    });
  };

  const handleSelectAllSubfilter = (event) => {
    let allItems = {};
    if (event.target.checked) {
      subfilterOptionsList.forEach((item) => {
        allItems[item.filter_value] = true;
      });
      setSelectedSubfilters(allItems);
      setShowAllSubFilteredItems(true);
    } else {
      setSelectedSubfilters({});
      setShowAllSubFilteredItems(false);
    }
  };

  useEffect(() => {
    // Get true subfilters
    let subFilters = Object.keys(selectedSubfilters).filter(
      (key) => selectedSubfilters[key]
    );
    // filter profiles based on subfilter key
    if (filteredProfiles) {
      let subfiltered = filteredProfiles.filter((profile) => {
        if (subFilters.includes(profile[subfiltersKey])) {
          return profile;
        }
      });

      setSubFilteredProfiles(subfiltered);
    }

    // Uncheck "All" if all filters are no longer selected
    subfilterOptionsList.forEach((item) => {
      if (!selectedSubfilters[item.filter_value]) {
        setShowAllSubFilteredItems(false);
      }
    });
  }, [selectedSubfilters]);

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
                onClick={() => {
                  filterProfiles(filter.filter_value);
                  setShowSubfilters(filter.enable_subfiltering);
                }}
                key={filter.filter_value}
              >
                {filter.filter_label}
              </button>
            ))}
          </div>
        </nav>
      </div>

      {!loading && filteredProfiles.length > 0 && subfilterOptionsList && (
        <div className="tw-w-max tw-mb-6 tw-relative" ref={subFiltersDropdown}>
          {subfiltersLabel && (
            <button
              id="subfilters-dropdown"
              onClick={() => setSubFiltersExpanded(!subFiltersExpanded)}
              className="tw-font-normal tw-text-[15px] tw-p-3 tw-flex tw-flex-row tw-justify-between tw-items-center tw-border tw-border-gray-20"
              aria-expanded={subFiltersExpanded}
              aria-haspopup="listbox"
            >
              <span>Filter By {subfiltersLabel}</span>
              <img
                className={`tw-w-4 tw-h-4 tw-ml-2 ${
                  subFiltersExpanded ? "tw-rotate-180" : ""
                }`}
                src="/static/_images/glyphs/down-chevron.svg"
                alt=""
              />
            </button>
          )}
          {subFiltersExpanded && (
            <div
              role="listbox"
              tabIndex="-1"
              className="tw-p-3 tw-pt-0 tw-absolute tw-top-[40px] tw-bg-white tw-w-full tw-z-10 tw-border-r tw-border-b tw-border-l tw-border-gray-20 tw-border-t-0"
              aria-labelledby="subfilters-dropdown"
            >
              {/*Show all*/}
              <div className="tw-pl-5" key={`show-all-subfilters-checkbox`}>
                <label className="form-check-label">
                  <input
                    className="form-check-input tw-mt-1"
                    type="checkbox"
                    checked={showAllSubFilteredItems}
                    value={getText("Show All")}
                    onChange={handleSelectAllSubfilter}
                  />
                  <div>{getText("Show All")}</div>
                </label>
              </div>
              {subfilterOptionsList.map((option) => (
                <div
                  className="tw-pl-5"
                  key={`${option.filter_value}-checkbox`}
                >
                  <label className="form-check-label">
                    <input
                      className="form-check-input tw-mt-1"
                      type="checkbox"
                      name={option.filter_value}
                      checked={selectedSubfilters[option.filter_value]}
                      value={option.filter_value}
                      onChange={(e) => {
                        handleSelectSubfilter(e);
                      }}
                    />
                    <div>{option.filter_label}</div>
                  </label>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div>
        {/* Loading */}
        {loading && <LoadingSpinner />}

        {/*If profiles are filtered with the subfilter show them instead*/}
        {subFilteredProfiles.length > 0 && (
          <div className="tw-grid large:tw-grid-cols-2 tw-mb-5 w-full tw-gap-6">
            {subFilteredProfiles.map((profile) => (
              <PulseProfile key={profile.id} profile={profile} />
            ))}
          </div>
        )}

        {/* Done loading and profiles exist */}
        {!loading &&
          filteredProfiles.length > 1 &&
          subFilteredProfiles.length < 1 && (
            <div className="tw-grid large:tw-grid-cols-2 tw-mb-5 w-full tw-gap-6">
              {filteredProfiles.map((profile) => (
                <PulseProfile key={profile.id} profile={profile} />
              ))}
            </div>
          )}

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
