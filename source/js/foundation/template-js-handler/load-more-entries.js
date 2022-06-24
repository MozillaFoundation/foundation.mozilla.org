/**
 * Bind click handler to ".load-more-index-entries"
 * (the "load more" button on index pages)
 */
export default () => {
  // Enable the "load more results" button on index pages
  let loadMoreButton = document.querySelector(`.load-more-index-entries`);
  if (loadMoreButton) {
    const entries = document.querySelector(`#index-entries`);

    // Get the page size from the document, which the IndexPage should
    // have templated into its button as a data-page-size attribute.
    const pageSize = parseInt(loadMoreButton.dataset.pageSize) || 12;

    // Get which page type or model to exclude, if any exist in the data-exclude
    // html attribute.
    const exclude = loadMoreButton.dataset.exclude || "";

    // Start at page 1, as page 0 is the same sat as the initial page set.
    let page = 1;

    const loadMoreResults = () => {
      loadMoreButton.disabled = true;

      // Construct our API call as a relative URL:
      let url = `./entries/?page=${page++}&page_size=${pageSize}&exclude=${exclude}`;

      // And then fetch the results and render them into the page.
      fetch(url)
        .then((result) => result.json())
        .then((data) => {
          if (!data.has_next) {
            loadMoreButton.removeEventListener(`click`, loadMoreResults);
            loadMoreButton.parentNode.removeChild(loadMoreButton);
          }
          return data.entries_html;
        })
        .then((entries_html) => {
          const div = document.createElement(`div`);
          div.innerHTML = entries_html;
          Array.from(div.children).forEach((c) => entries.appendChild(c));
        })
        .catch((err) => {
          // TODO: what do we want to do in this case?
          console.error(err);
        })
        .finally(() => {
          loadMoreButton.disabled = false;
        });
    };

    loadMoreButton.addEventListener(`click`, loadMoreResults);
  }
};
