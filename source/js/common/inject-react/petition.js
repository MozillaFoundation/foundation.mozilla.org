import { createRoot } from "react-dom/client";
import Petition from "../../components/petition/petition.jsx";

/**
 * Inject petition forms
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 * @param {String} siteUrl Foundation site base URL
 */
export default (apps, siteUrl) => {
  // petition elements
  var subscribed = false;

  if (window.location.search.indexOf(`subscribed=1`) !== -1) {
    subscribed = true;
  }

  document.querySelectorAll(`.sign-petition`).forEach((element) => {
    var props = element.dataset;

    props.apiUrl = `${siteUrl}/api/campaign/petitions/${props.petitionId}/`;

    apps.push(
      new Promise((resolve) => {
        const root = createRoot(element);
        root.render(
          <Petition
            {...props}
            isHidden={false}
            subscribed={subscribed}
            whenLoaded={() => resolve()}
          />
        );
      })
    );
  });
};
