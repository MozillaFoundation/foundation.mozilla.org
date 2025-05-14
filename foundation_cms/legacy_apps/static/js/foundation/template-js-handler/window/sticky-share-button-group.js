/**
 * Bind scroll handler to window to toggle sticky share buttons on blog page
 */
export default () => {
  let blogPageStickyButtons = document.querySelector(
    `#view-blog .blog-sticky-side .share-button-group`
  );
  let blogPageFullButtons = document.querySelector(
    `.bottom-share-button-container .share-button-group`
  );

  if (blogPageStickyButtons && blogPageFullButtons) {
    const isInViewport = (element) => {
      let box = element.getBoundingClientRect();

      return box.top <= window.innerHeight && box.top + box.height >= 0;
    };

    const toggleStickyButtons = () => {
      if (isInViewport(blogPageFullButtons)) {
        blogPageStickyButtons.classList.add(`faded`);
      } else {
        blogPageStickyButtons.classList.remove(`faded`);
      }
    };

    window.addEventListener(`scroll`, toggleStickyButtons, { passive: true });

    toggleStickyButtons();
  }
};
