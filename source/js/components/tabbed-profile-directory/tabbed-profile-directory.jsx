import React, {useEffect, useState} from 'react'

 const TabbedProfileFilters = ({apiEndPoint, filterKey, filterOptions, subFilters, whenLoaded}) => {

 const filterOptionsList = JSON.parse(filterOptions).map((filterOption) => filterOption.fields)

    // Component is loaded
    useEffect(() => {
      // This component has been loaded and resolve promise
      whenLoaded()
    }, [])

    return (
      <div>
        <div className="my-2">
          <h2>Filter Options</h2>
          {filterOptionsList.map((filter, index) => (
              <button key={index}>{filter.filter_label}</button>
          ))}
        </div>
        <div className="my-2">
          <h2>SubFilters</h2>
          <pre>{subFilters}</pre>
        </div>
      </div>
    )
  }

  export default TabbedProfileFilters
