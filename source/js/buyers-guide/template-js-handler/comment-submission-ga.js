/**
 * PNI product pages use commento to handle comment submissions.
 * This file adds a handler in order to fire a GA event if the user logs into commento and submits a comment.
 */
export default () => {
  const commentoContainer = document.querySelector(
    "#view-product-page #commento"
  );
  console.log(commentoContainer)
  const submitButton = commentoContainer.querySelector(
    "#commento-submit-button-root"
  );

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

  if (commentoContainer && submitButton) {

    submitButton.addEventListener(`click`, () => {

      commentSubmittedEvent()
    });
  }
};
