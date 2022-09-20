/**
 * PNI product pages use commento.io (https://commento.io/) to handle comment submissions.
 * Since at the moment there is no official callback for comment submission through commento itself,
 * we have this file which will push a datalayer event whenever a user submits a comment.
 */
export default () => {
  const commentoContainer = document.querySelector(
    "#view-product-page #commento"
  );
  const submitButton = commentoContainer.querySelector(
    "#commento-submit-button-root"
  );

  if (commentoContainer && submitButton) {
    submitButton.addEventListener(`click`, () => {
      commentSubmittedEvent()
    });
  }

  function commentSubmittedEvent() {
      // Checking if the user is logged in. If so, we can
      // assume it is safe to fire the GA event.
      let loggedInContainer = commentoContainer.querySelector(
        "#commento-logged-container"
      );

      if (loggedInContainer) {

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
