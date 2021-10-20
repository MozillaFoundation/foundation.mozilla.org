import React, { useEffect, useState, useRef } from "react";
import PulseProfile from "../pulse-profile/pulse-profile";
import LoadingSpinner from "./loading-spinner";
import { getText } from "./locales";
import SubfilterDropdown from "./subfilter-dropdown";
import FiltersNav from "./filters-nav";

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
  const [loading, setLoading] = useState(true);
  const [filteredProfiles, setFilteredProfiles] = useState([]);
  const [currentFilterValue, setCurrentFilterValue] = useState(null);
  const [subFilteredProfiles, setSubFilteredProfiles] = useState([]);
  const [selectedSubfilters, setSelectedSubfilters] = useState({});
  const [showAllSubFilteredItems, setShowAllSubFilteredItems] = useState(null);
  const [enableSubfiltering, setEnableSubFiltering] = useState(false);

  // Component is loaded
  useEffect(() => {
    // This component has been loaded and resolve promise
    whenLoaded();
    setLoading(false);

    // Set initial filtered profiles from django
    if (profiles) {
      setFilteredProfiles(profiles);
    }

    // Initial profiles are the first tab so grab the subfiltering option for the first tab
    if (filterOptionsList) {
      if (filterOptionsList[0].enable_subfiltering === true) {
        setEnableSubFiltering(true);
      }
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

    // Empty Filtered and Subfiltered items
    setFilteredProfiles([]);
    setSubFilteredProfiles([]);
    setSelectedSubfilters({});

    // Retrieve api data
    const data = await getData(filterValue);

    // Set filtered profiles state
    if (data) {
      setFilteredProfiles(data);
    }

    document.dispatchEvent(new CustomEvent("profiles:list-updated"));
  };

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
    // Get array of subfilters
    let subfilters = Object.keys(selectedSubfilters).filter(
      (key) => selectedSubfilters[key]
    );
    // filter profiles based on subfilter key
    if (filteredProfiles) {
      let subfiltered = filteredProfiles.filter((profile) => {
        if (subfilters.includes(profile[subfiltersKey])) {
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
      <FiltersNav
        filters={filterOptionsList}
        currentFilterValue={currentFilterValue}
        onFilterClick={(filter) => {
          filterProfiles(filter.filter_value);
          setEnableSubFiltering(filter.enable_subfiltering);
        }}
      />

      {enableSubfiltering &&
        !loading &&
        filteredProfiles.length > 0 &&
        subfilterOptionsList && (
          <SubfilterDropdown
            label={subfiltersLabel}
            showAll={showAllSubFilteredItems}
            onChangeShowAll={(e) => handleSelectAllSubfilter(e)}
            onChangeSubfilter={(e) => handleSelectSubfilter(e)}
            subfilters={subfilterOptionsList}
            selectedFilters={selectedSubfilters}
          />
        )}

      {/* Cards Block */}
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
