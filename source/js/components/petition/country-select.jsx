import React from 'react';
import classNames from 'classnames';
import SALESFORCE_COUNTRY_LIST from './salesforce-country-list.js';

export default class CountrySelect extends React.Component {
  render() {
    let className = classNames(`form-label-group`, `country-picker`, this.props.className);
    let codes = Object.keys(SALESFORCE_COUNTRY_LIST);
    let options = codes.map( code => {
      return <option key={code} value={code}>{SALESFORCE_COUNTRY_LIST[code]}</option>;
    });

    return (
      <div className={className}>
        <select className="form-control"
          disabled={this.props.disabled}
          ref={(element) => { this.element = element; }}
          onFocus={this.props.onFocus}
          defaultValue={``}
        >
          <option value="">{this.props.label}</option>
          { options }
        </select>
      </div>
    );
  }
}
