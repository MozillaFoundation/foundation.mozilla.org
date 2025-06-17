import SALESFORCE_COUNTRY_LIST from "./salesforce-country-list.js";

let countryDefault = { value: "", label: "Your Country" };
let countryOptions = Object.keys(SALESFORCE_COUNTRY_LIST).map((code) => {
  return {
    value: code,
    label: SALESFORCE_COUNTRY_LIST[code],
  };
});
countryOptions.unshift(countryDefault);

export const COUNTRY_OPTIONS = countryOptions;
