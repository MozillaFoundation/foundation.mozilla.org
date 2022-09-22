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

  const commentListUpdateHandler = (mutations) => {
    let commentList = document.querySelector("#commento-main-area");

    mutations.forEach(function (mutation) {
      // If there was a added node to the comment list container div, push the datalayer event.
      if ((mutation.target == commentList) && mutation.addedNodes.length) {

        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
          event: "form_submission",
          form_name: commentoContainer.getAttribute("data-product-name"),
          form_location: window.location.host + window.location.pathname,
          form_type: "comment",
        });
        
      }
    });
  };

  const commentoFormHasBeenLoadedIn = () => {
    // Stop listening to the parent div for any activity.
    commentoParentDivObserver.disconnect();

    // Instead create a new observer that listens for updates to the comments list.
    const commentListObserver = new MutationObserver(commentListUpdateHandler);
    commentListObserver.observe(commentoContainer, {
      childList: true,
      subtree:true
    });
  };

  // Listen to the Commento container div for any updates within.
  const commentoParentDivObserver = new MutationObserver(commentoFormHasBeenLoadedIn);
  commentoParentDivObserver.observe(commentoContainer, {
    childList: true,
    subtree: true,
    attributes: true,
    characterData: true,
  });
};
