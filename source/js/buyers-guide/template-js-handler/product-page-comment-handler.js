/**
 * PNI product pages use commento.io (https://commento.io/) to handle comment submissions.
 * Since at the moment there is no official callback for comment submission through commento itself,
 * we have this file which will push a datalayer event whenever a user submits a comment.
 */
export default () => {
  const commentoContainer = document.querySelector(
    "#view-product-page #commento"
  );
  const submitButton = document.querySelector("#commento-submit-button-root");

  if (commentoContainer && submitButton) {
    submitButton.addEventListener(`click`, () => {
      commentSubmitted();
    });
  }

  function commentSubmitted() {
    // Checking if the user is logged in and if the text box has a value. 
    // If so, push the DataLayer event.
    let loggedInContainer = document.querySelector(
      "#commento-logged-container"
    );
    let textBoxValue = document.querySelector("#commento-textarea-root").value;

    if (loggedInContainer && textBoxValue) {
      window.dataLayer = window.dataLayer || [];

      window.dataLayer.push({
        event: "form_submission",
        form_name: commentoContainer.getAttribute("data-product-name"),
        form_location: window.location.host + window.location.pathname,
        form_type: "comment",
      });
    }
  }
};
