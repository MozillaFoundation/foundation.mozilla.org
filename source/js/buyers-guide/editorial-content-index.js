import 'htmx.org'

function main(){
  switchFromPaginationToLoadMore()

  htmx.onLoad(() => {
    // Define what needs to happen whenever new content is added to the DOM.

    // We need to configure this every time, because the button elements are destroyed
    // and replace with a new element in the response.
    setupLoadMoreButtonDisablingOnRequest()
  })
}

function switchFromPaginationToLoadMore(){
  const loadMore = document.getElementById('load-more')
  const pagination = document.getElementById('pagination')

  if (loadMore && pagination) {
    loadMore.classList.remove('tw-hidden')
    pagination.classList.add('tw-hidden')
  }
}

function setupLoadMoreButtonDisablingOnRequest() {
  // Disable the load more button when the request is triggered.
  // This is a signal to the user an prevents duplicate triggering.
  // We don't need to reactivate the button because it is replaced with the response.
  const loadMore = document.getElementById('load-more')

  if (!loadMore) {
   return
  }

  const loadMoreButton = loadMore.getElementsByTagName('button')[0]
  loadMoreButton.addEventListener('htmx:beforeRequest', (event) => {
    event.target.setAttribute('disabled', '')
  })
}

main()
