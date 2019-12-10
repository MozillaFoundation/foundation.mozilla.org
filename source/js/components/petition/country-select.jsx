import React from "react";
import classNames from "classnames";
import SALESFORCE_COUNTRY_LIST from "./salesforce-country-list.js";
import { t } from "@lingui/macro";
import { i18n } from "../i18n/catalogs-loader.jsx";

export default class CountrySelect extends React.Component {
  constructor(props) {
    super(props);
  }

  handleChange(event) {
    this.props.handleCountryChange(event.target.value);
  }

  render() {
    let classes = classNames(
      `country-picker form-control`,
      this.props.className
    );
    let codes = Object.keys(SALESFORCE_COUNTRY_LIST);
    let options = codes.map(code => {
      return (
        <option key={code} value={code}>
          {SALESFORCE_COUNTRY_LIST[code]}
        </option>
      );
    });

    return (
      <select
        className={classes}
        disabled={this.props.disabled}
        ref={element => {
          this.element = element;
        }}
        onFocus={this.props.onFocus}
        defaultValue={``}
        onChange={evt => this.handleChange(evt)}
        aria-label={i18n._(t`Please select your country`)}
      >
        <option value="">{this.props.label}</option>
        {options}
      </select>
    );
  }
}
