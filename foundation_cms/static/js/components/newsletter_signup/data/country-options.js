import SALESFORCE_COUNTRY_LIST from "./salesforce-country-list.js";

let localized_your_country = gettext("Your Country");
let countryDefault = { value: "", label: localized_your_country };
let countryOptions = Object.keys(SALESFORCE_COUNTRY_LIST).map((code) => {
  return {
    value: code,
    label: SALESFORCE_COUNTRY_LIST[code],
  };
});
countryOptions.unshift(countryDefault);

export const COUNTRY_OPTIONS = countryOptions;
