/**
 * PNI product pages use commento.io (https://commento.io/) to handle comment submissions.
 * Since at the moment there is no official callback for comment submission through commento itself,
 * we have this file which will push a datalayer event whenever a user submits a comment.
 */
 export default () => {
  // Commento's parent div, in which it loads all of its content through JS.
  const commentoContainer = document.querySelector(
    "#view-product-page #commento"
  );
  // The products initial count of comments, which we will use to compare against the new number
  let commentCount;


  const mutationHandler = (mutations) => {
  // Since commento sometimes does not load its contents before we run this JS file,
  // We are using this mutation handler to wait for a change in its parent div, 
  // whether it be an item loading in, the user typing in the text box, etc, 
  // so we know the content has loaded in, and its safe to add the event handlers 
  // and define the initial count of comments. Then disconnecting the mutation handler.
    let submitButton = document.querySelector("#commento-submit-button-root");
    commentCount = document.querySelectorAll('.commento-card').length;

    submitButton.addEventListener(`click`, () => {
      submitButtonClicked();
    });

    mutationObserver.disconnect()
  };

  const mutationObserver = new MutationObserver(mutationHandler);
  mutationObserver.observe(commentoContainer, { childList:true, subtree: true, attributes:true ,characterData:true });

  function submitButtonClicked() {

    let newCommentCount = document.querySelectorAll('.commento-card').length;

    // Ideally the list of comments would update, and we can compare these two numbers.
    // However, since I am assuming commento is making a api call to post the comment, 
    // The list does not get updated in time.
    if(newCommentCount > commentCount){

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
