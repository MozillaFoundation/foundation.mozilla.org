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

  if (!commentoContainer) {
    return;
  }

  const commentListUpdateHandler = (mutations) => {
    mutations.forEach(function (mutation) {
      // New comments are appended in the form of: <div><div class='commento-card'/></div>
      // If comment tracking ever breaks, this logic would be a good place to check first.
      // For more context, see: https://github.com/mozilla/foundation.mozilla.org/pull/9414
      if (mutation.addedNodes[0]?.firstChild?.matches(".commento-card")) {
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

  // Listen to the Commento container div for any updates such as:
  // Added nodes, removed nodes, etc.
  const commentListObserver = new MutationObserver(commentListUpdateHandler);
  commentListObserver.observe(commentoContainer, {
    childList: true,
    subtree: true,
  });
};
