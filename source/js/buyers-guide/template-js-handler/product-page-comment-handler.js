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
    // The div which new comments get appended to.
    let commentList = document.querySelector("#commento-main-area");

    mutations.forEach(function (mutation) {
      // New comment mutations come in the form of a single added node, with no attributes.
      let newNodeAttributes = mutation.addedNodes[0].attributes;
      if ((newNodeAttributes.length == 0) && (mutation.target == commentList)) {

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



  // Listen to the Commento container div for any updates within.
  const commentListObserver = new MutationObserver(commentListUpdateHandler);
  commentListObserver.observe(commentoContainer, {
    childList: true,
    subtree: true
  });
};
