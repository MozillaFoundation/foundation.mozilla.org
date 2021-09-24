import React from "react";
import ReactDOM from "react-dom";
import ProductTabs from "../components/product-tabs/product-tabs.jsx";

/**
 * Inject creep vote section
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 * @param {String} siteUrl Foundation site base URL
 */
export default (apps, siteUrl) => {
  document.querySelectorAll(`.product-tabs-target`).forEach((element) => {
    console.log(element.dataset.productInfo);
    apps.push(
      new Promise((resolve) => {
        ReactDOM.render(<ProductTabs />, element);
      })
    );
  });
};
