import React, { useEffect, useRef, useState } from "react";
import { getText } from "./locales";

const SubfilterDropdown = ({
  label,
  showAll,
  onChangeShowAll,
  onChangeSubfilter,
  subfilters,
  selectedFilters,
}) => {
  const subFiltersDropdown = useRef(null);
  const [dropdownExpanded, setDropdownExpanded] = useState(false);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (subFiltersDropdown) {
        if (!subFiltersDropdown.current.contains(event.target)) {
          setDropdownExpanded(false);
        }
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
  }, [subFiltersDropdown]);

  // Close subFilters with escape
  useEffect(() => {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        setDropdownExpanded(false);
      }
    });
  }, []);

  return (
    <div className="tw-w-max tw-mb-6 tw-relative" ref={subFiltersDropdown}>
      {label && (
        <button
          id="subfilters-dropdown"
          onClick={() => setDropdownExpanded(!dropdownExpanded)}
          className="tw-font-normal tw-text-[15px] tw-p-3 tw-flex tw-flex-row tw-justify-between tw-items-center tw-border tw-border-gray-20"
          aria-expanded={dropdownExpanded}
          aria-haspopup="listbox"
        >
          <span>Filter By {label}</span>
          <img
            className={`tw-w-4 tw-h-4 tw-ml-2 ${
              dropdownExpanded ? "tw-rotate-180" : ""
            }`}
            src="/static/_images/glyphs/down-chevron.svg"
            alt=""
          />
        </button>
      )}
      {dropdownExpanded && (
        <div
          role="listbox"
          tabIndex="-1"
          className="tw-p-3 tw-pt-0 tw-absolute tw-top-[40px] tw-bg-white tw-w-full tw-z-10 tw-border-r tw-border-b tw-border-l tw-border-gray-20 tw-border-t-0"
          aria-labelledby="subfilters-dropdown"
        >
          {/*Show all*/}
          <div className="tw-pl-5" key={`show-all-subfilters-checkbox`}>
            <label className="form-check-label hover:tw-cursor-pointer">
              <input
                className="form-check-input tw-mt-1"
                type="checkbox"
                name="show-all"
                checked={showAll}
                value={getText("Show All")}
                onChange={onChangeShowAll}
              />
              <div>{getText("Show All")}</div>
            </label>
          </div>
          {subfilters.map((option) => (
            <div className="tw-pl-5" key={`${option.filter_value}-checkbox`}>
              <label className="form-check-label hover:tw-cursor-pointer">
                <input
                  className="form-check-input tw-mt-1"
                  type="checkbox"
                  name={option.filter_value}
                  checked={selectedFilters[option.filter_value] || false}
                  value={option.filter_value}
                  onChange={(e) => {
                    onChangeSubfilter(e);
                  }}
                />
                <div>{option.filter_label}</div>
              </label>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SubfilterDropdown;
