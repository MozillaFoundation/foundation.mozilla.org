import React from "react";
import { createRoot } from "react-dom/client";
import BlogBodySignupForm from "../../components/newsletter-signup/organisms/blog-body-signup.jsx";

/**
 * Inject newsletter signup forms
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 * @param {String} siteUrl Foundation site base URL
 */
export default (apps, siteUrl) => {
  document
    .querySelectorAll(`.newsletter-signup-module[data-module-type="blog-body"]`)
    .forEach((element) => {
      const props = element.dataset;
      const sid = props.signupId || 0;

      props.apiUrl = `${siteUrl}/api/campaign/signups/${sid}/`;
      props.isHidden = false;

      apps.push(
        new Promise((resolve) => {
          const root = createRoot(element);
          root.render(
            <BlogBodySignupForm {...props} whenLoaded={() => resolve()} />
          );
        })
      );
    });
};
