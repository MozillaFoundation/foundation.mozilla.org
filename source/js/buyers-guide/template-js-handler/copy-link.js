import copyToClipboard from "../../../js/copy-to-clipboard.js";

/**
 * Bind click handler to ".copy-link"
 */
export default () => {
  document.querySelectorAll(`.copy-link`).forEach((element) => {
    element.addEventListener(`click`, (event) => {
      event.preventDefault();

      copyToClipboard(event.target, window.location.href);
    });
  });
};
