import { createRoot } from "react-dom/client";
import PetitionThankYou from "../../components/petition/petition-thank-you.jsx";

/**
 * Inject thank you screen for FormAssembly petition forms
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 */
export default (apps) => {
  document
    .querySelectorAll(`.formassembly-petition-thank-you`)
    .forEach((element) => {
      var props = element.dataset;

      apps.push(
        new Promise((resolve) => {
          const root = createRoot(element);
          root.render(
            <PetitionThankYou {...props} whenLoaded={() => resolve()} />
          );
        })
      );
    });
};
