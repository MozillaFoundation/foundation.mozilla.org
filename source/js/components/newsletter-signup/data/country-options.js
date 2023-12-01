import SALESFORCE_COUNTRY_LIST from "../../petition/salesforce-country-list.js";
import { getText } from "../../petition/locales";

let countryDefault = { value: "", label: getText(`Your country`) };
let countryOptions = Object.keys(SALESFORCE_COUNTRY_LIST).map((code) => {
  return {
    value: code,
    label: SALESFORCE_COUNTRY_LIST[code],
  };
});
countryOptions.unshift(countryDefault);

export const COUNTRY_OPTIONS = countryOptions;
