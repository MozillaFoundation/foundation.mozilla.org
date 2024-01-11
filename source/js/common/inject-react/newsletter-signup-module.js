import React from "react";
import { createRoot } from "react-dom/client";
import DefaultSignupForm from "../../components/newsletter-signup/organisms/default-layout-signup.jsx";

/**
 * Inject newsletter signup forms
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 * @param {String} siteUrl Foundation site base URL
 */
export default (apps, siteUrl) => {
  // excluding `.newsletter-signup-module.on-nav` because it's taken care of by nav-newsletter.js
  document
    .querySelectorAll(`.newsletter-signup-module:not(.on-nav)`)
    .forEach((element) => {
      const props = element.dataset;
      const sid = props.signupId || 0;
      const moduleType = props.moduleType;
      let Form;

      props.apiUrl = `${siteUrl}/api/campaign/signups/${sid}/`;
      props.isHidden = false;

      if (moduleType === "default") {
        Form = DefaultSignupForm;
      }

      if (Form) {
        apps.push(
          new Promise((resolve) => {
            const root = createRoot(element);
            root.render(<Form {...props} whenLoaded={() => resolve()} />);
          })
        );
      }
    });
};
