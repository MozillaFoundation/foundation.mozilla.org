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
      if (subFiltersDropdown.current) {
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
    <div
      className="tw-w-max tw-mb-16 tw-relative tw-min-w-[275px]"
      ref={subFiltersDropdown}
    >
      {label && (
        <button
          id="subfilters-dropdown"
          onClick={() => setDropdownExpanded(!dropdownExpanded)}
          className="tw-font-normal tw-text-[15px] tw-p-6 tw-flex tw-flex-row tw-justify-between tw-items-center tw-border tw-border-gray-20 tw-w-full"
          aria-expanded={dropdownExpanded}
          aria-haspopup="listbox"
        >
          <span>
            {getText("Filter by ")}
            {label}
          </span>
          <img
            className={`tw-w-8 tw-h-8 tw-ml-4 ${
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
          className="tw-p-6 tw-pt-0 tw-absolute tw-top-20 tw-bg-white tw-w-full tw-z-10 tw-border-r tw-border-b tw-border-l tw-border-gray-20 tw-border-t-0"
          aria-labelledby="subfilters-dropdown"
        >
          {/*Show all*/}
          <div
            className="tw-pl-16 tw-py-4 tw-relative"
            key={`show-all-subfilters-checkbox`}
          >
            <input
              className="profile-subfilter-checkbox tw-mt-1"
              type="checkbox"
              name="show-all"
              checked={showAll}
              value={getText("Show All")}
              onChange={onChangeShowAll}
            />
            <label className="form-check-label hover:tw-cursor-pointer">
              <span className="checkbox" />
              <div>{getText("Show All")}</div>
            </label>
          </div>
          {subfilters.map((option) => (
            <div
              className="tw-pl-16 tw-py-4 tw-relative"
              key={`${option.filter_value}-checkbox`}
            >
              <input
                className="profile-subfilter-checkbox tw-mt-1"
                type="checkbox"
                name={option.filter_value}
                checked={selectedFilters[option.filter_value] || false}
                value={option.filter_value}
                onChange={(e) => {
                  onChangeSubfilter(e);
                }}
              />
              <label className="form-check-label hover:tw-cursor-pointer">
                <span className="checkbox" />
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
