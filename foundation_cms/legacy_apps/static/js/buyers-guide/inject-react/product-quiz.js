import React from "react";
import { createRoot } from "react-dom/client";
import ProductQuiz from "../components/product-quiz/product-quiz.jsx";

/**
 * Inject product quiz React component
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 */
export default (apps, siteUrl) => {
  document.querySelectorAll(`.product-quiz-wrapper`).forEach((element) => {
    apps.push(
      new Promise((resolve) => {
        const root = createRoot(element);
        root.render(
          <ProductQuiz
            {...element.dataset}
            whenLoaded={() => resolve()}
            joinUsApiUrl={`${siteUrl}/api/campaign/signups/0/`}
            pniHomeUrl={`${siteUrl}/privacynotincluded/`}
          />
        );
      })
    );
  });
};
