import React from "react";
import classNames from "classnames";
import SALESFORCE_COUNTRY_LIST from "./salesforce-country-list.js";
import { Localized } from "../localized.js";

export default class CountrySelect extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let classes = classNames(
      `country-picker form-control`,
      this.props.className
    );
    let codes = Object.keys(SALESFORCE_COUNTRY_LIST);
    let options = codes.map((code) => {
      return (
        <option key={code} value={code}>
          {SALESFORCE_COUNTRY_LIST[code]}
        </option>
      );
    });

    return (
      <Localized stringId="select-country" attrs={{ "aria-label": true }}>
        <select
          className={classes}
          disabled={this.props.disabled}
          ref={(element) => {
            this.element = element;
          }}
          onFocus={this.props.onFocus}
          defaultValue={``}
          aria-label="Please select your country"
        >
          <option value="">{this.props.label}</option>
          {options}
        </select>
      </Localized>
    );
  }
}
