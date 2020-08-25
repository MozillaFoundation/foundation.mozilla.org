import React from "react";
import ReactDOM from "react-dom";
import CreepVote from "../components/creep-vote/creep-vote.jsx";

/**
 * Inject creep vote section
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 * @param {String} siteUrl Foundation site base URL
 * @param {String} csrfToken CSRF Token
 */
export default (apps, siteUrl, csrfToken) => {
  document.querySelectorAll(`.creep-vote-target`).forEach((element) => {
    let csrf = element.querySelector(`input[name=csrfmiddlewaretoken]`);
    let productType = element.dataset.productType;
    let productName = element.dataset.productName;
    let productID = element.querySelector(`input[name=productID]`).value;
    let votesValue = element.querySelector(`input[name=votes]`).value;

    let votes = {
      total: 0,
      creepiness: {
        average: 50,
        vote_breakdown: { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0 },
      },
      confidence: { 0: 0, 1: 0 },
    };

    if (votesValue !== "None") {
      try {
        votes = JSON.parse(votesValue.replace(/'/g, `"`));
      } catch (e) {
        // if this fails, we just use the defaults
      }
    }

    apps.push(
      new Promise((resolve) => {
        ReactDOM.render(
          <CreepVote
            csrf={csrf.value}
            productType={productType}
            productName={productName}
            productID={parseInt(productID, 10)}
            votes={votes}
            whenLoaded={() => resolve()}
            joinUsCSRF={csrfToken}
            joinUsApiUrl={`${siteUrl}/api/campaign/signups/0/`}
          />,
          element
        );
      })
    );
  });
};
