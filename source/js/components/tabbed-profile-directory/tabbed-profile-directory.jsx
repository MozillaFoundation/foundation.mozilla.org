import React, {useEffect, useState, useRef} from "react";
import PulseProfile from "../pulse-profile/pulse-profile";
import LoadingSpinner from "./loading-spinner";
import {getText} from "./locales";

const TabbedProfileFilters = ({
                                apiEndPoint,
                                filterKey,
                                filterOptions,
                                subFilters,
                                subfiltersLabel,
                                whenLoaded,
                                profiles,
                              }) => {

  const filterOptionsList = JSON.parse(filterOptions).map(
    (filterOption) => filterOption.fields
  );
  const subfilterOptionsList = JSON.parse(subFilters).map(
    (option) => option.fields
  );
  const [filteredProfiles, setFilteredProfiles] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentFilterValue, setCurrentFilterValue] = useState(null);
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

    // make sure that "back" does the right thing.
    window.addEventListener("popstate", (evt) => {
      const state = evt.state;
      if (!state) {
        return;
      }
      filterProfiles(state.type);
    });

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
      if (e.key === 'Escape') {
        setSubFiltersExpanded(false);
      }
    })
  }, [])


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

      {!loading && filteredProfiles.length > 0 && subfilterOptionsList &&
      (<div className="tw-w-max tw-mb-6 tw-relative" ref={subFiltersDropdown}>
          {subfiltersLabel &&
          <button
            id="subfilters-dropdown"
            onClick={() => setSubFiltersExpanded(!subFiltersExpanded)}
            className="tw-font-normal tw-text-[15px] tw-p-3 tw-flex tw-flex-row tw-justify-between tw-items-center tw-border tw-border-gray-20"
            aria-expanded={subFiltersExpanded}
            aria-haspopup="listbox">
            <span>Filter By {subfiltersLabel}</span>
            <img className={`tw-w-4 tw-h-4 tw-ml-2 ${subFiltersExpanded ? 'tw-rotate-180' : ''}`} src="/static/_images/glyphs/down-chevron.svg" alt=""/>
          </button>}
          {subFiltersExpanded &&
          <div role="listbox"
               tabindex="-1"
               className="tw-p-3 tw-pt-0 tw-absolute tw-top-[40px] tw-bg-white tw-w-full tw-z-10 tw-border-r tw-border-b tw-border-l tw-border-gray-20 tw-border-t-0"
               aria-labelledby="subfilters-dropdown">
            {subfilterOptionsList.map((option) => (
              <div className="tw-pl-5" key={`${option.filter_value}-checkbox`}>
                <label className="form-check-label">
                  <input
                    className="form-check-input tw-mt-1"
                    type="checkbox"
                    checked={option.isChecked}
                    value={option.filter_value}
                  />
                  <div>{option.filter_label}</div>
                </label>
              </div>
            ))}
          </div>
          }
        </div>
      )}

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
