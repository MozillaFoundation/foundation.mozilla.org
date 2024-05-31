import SALESFORCE_COUNTRY_LIST from "../../petition/salesforce-country-list.js";

let countryDefault = { value: "", label: gettext("Your country") };
let countryOptions = Object.keys(SALESFORCE_COUNTRY_LIST).map((code) => {
  return {
    value: code,
    label: SALESFORCE_COUNTRY_LIST[code],
  };
});
countryOptions.unshift(countryDefault);

export const COUNTRY_OPTIONS = countryOptions;
